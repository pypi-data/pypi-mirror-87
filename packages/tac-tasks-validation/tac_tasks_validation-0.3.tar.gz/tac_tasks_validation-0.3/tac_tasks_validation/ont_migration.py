import logging

from tac_tasks_validation.base import ValidateOldOnt, ValidateNewOnt
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor
from tac_tasks_validation.exceptions import ActiveSessionError


class ONTMigrationValidation(ValidateOldOnt, ValidateNewOnt):
    """ Validates OLD ONT for migration from old to new system/db """

    def __init__(
            self,
            ont_sn: str,
            logger: logging.Logger,
            old_db_session: Session,
            old_db_radius_session: Session,
            new_db_session: Session
    ):
        """
        Validates the ONT exists on the old db only and there is no active session on it
        If the validation succeeds then instance attribute `old_service_table_data` will contain
        the OLD DB Service table data
        :param ont_sn: ONT Serial number
        :param logger: logging object
        :param old_db_session: OLD DB Service table session object
        :param old_db_radius_session: OLD DB Radius table session object
        :param new_db_session: NEW DB ONT table session object
        """
        self.ont_sn = ont_sn
        self.logger = logger
        self.old_db_session = old_db_session
        self.old_db_radius_session = old_db_radius_session
        self.new_db_session = new_db_session
        self.old_service_table_data = None
        super(ONTMigrationValidation, self).__init__(
            old_ont=ont_sn,
            old_db_session=old_db_session,
            old_db_radius_session=old_db_radius_session,
            logger=logger
        )
        super(ValidateOldOnt, self).__init__(
            new_ont=ont_sn,
            new_db_session=new_db_session,
            logger=logger
        )

    def validate_old_exists(self):
        try:
            super(ONTMigrationValidation, self).validate_old_exists()
        except ActiveSessionError:
            pass

    def validate_ont_migration(self):
        """
        Validates ONT for ONT migration
        :return: None
        :raise ValidationError: If any validation error
        """

        with ThreadPoolExecutor(max_workers=2) as executor:
            old_validate = executor.submit(self.validate_old_exists)
            new_validate = executor.submit(self.validate_new_not_exists)
            old_exception = old_validate.exception()
            new_exception = new_validate.exception()

        if old_exception:
            raise old_exception

        if new_exception:
            raise new_exception

        self.old_service_table_data = self.old_ont_data

        return None
