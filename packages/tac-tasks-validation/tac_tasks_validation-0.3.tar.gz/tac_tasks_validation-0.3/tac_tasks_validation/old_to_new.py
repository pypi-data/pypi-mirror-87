import logging

from fibrenest_db_models.postgres import ONTSWAP
from sqlalchemy import or_
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor
from tac_tasks_validation.exceptions import ValidationError, ActiveSessionError
from typing import List
from tac_tasks_validation.base import ValidateNewOnt, ValidateOldOnt


class OltToNewValidation(ValidateOldOnt, ValidateNewOnt):
    """ Validates OLD to New swap ONTs """

    def __init__(
            self,
            old_ont: str,
            new_ont: str,
            logger: logging.Logger,
            old_db_session: Session,
            old_db_radius_session: Session,
            new_db_session: Session
    ):
        """
        Validates OLD and NEW ONTs for swap process. If the validation succeeds then instance
        attribute `old_service_table_data` will contain the OLD DB Service table data and
        the attribute `new_ont_table_data` will contain the NEW DB Ont table data
        :param old_ont: OLD ONT Serial number
        :param new_ont: NEW ONT Serial number
        :param logger: logging object
        :param old_db_session: OLD DB Service table session object
        :param old_db_radius_session: OLD DB Radius table session object
        :param new_db_session: NEW DB ONT table session object
        """

        self.old_ont = old_ont
        self.new_ont = new_ont
        self.logger = logger
        self.old_db_session = old_db_session
        self.old_db_radius_session = old_db_radius_session
        self.new_db_session = new_db_session
        self.old_service_table_data = None
        self.new_ont_table_data = None
        super(OltToNewValidation, self).__init__(
            old_ont=old_ont,
            old_db_session=old_db_session,
            old_db_radius_session=old_db_radius_session,
            logger=logger
        )
        super(ValidateOldOnt, self).__init__(
            new_ont=new_ont,
            new_db_session=new_db_session,
            logger=logger
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(old_ont={self.old_ont},new_ont={self.new_ont})'

    def onts_not_already_for_swap(self):
        """ Checks the either OLD or NEW ONT arent already scheduled for a swap """

        query: List[ONTSWAP] = self.new_db_session.query(ONTSWAP).filter(
            or_(ONTSWAP.old_sn == self.old_ont, ONTSWAP.new_sn == self.new_ont),
            or_(ONTSWAP.swap_status == 'pending', ONTSWAP.swap_status == 'started')
        ).all()
        if query:
            raise ValidationError(
                f'ONT Swap for these ONTs already scheduled. JOB ID for these are: {[q.id for q in query]}'
            )

    def validate_old_exists(self):
        try:
            super(OltToNewValidation, self).validate_old_exists()
        except ActiveSessionError as active_error:
            raise ValidationError(str(active_error)) from None

    def validate_old_to_new_swap(self):
        """
        Performs some validation like checking the ONTs still exists in DB and service status hasn't changed
        :return: None
        :raise ValidationError: If any validation error
        :raise CantProceedError: If we cant proceed with the swap. This isn't an error as such
        """

        with ThreadPoolExecutor(max_workers=2) as executor:
            old_validate = executor.submit(self.validate_old_exists)
            new_validate = executor.submit(self.validate_new_exists)
            old_exception = old_validate.exception()
            new_exception = new_validate.exception()

        if old_exception:
            raise old_exception

        if new_exception:
            raise new_exception

        self.old_service_table_data = self.old_ont_data
        self.new_ont_table_data = self.new_ont_data

        return None
