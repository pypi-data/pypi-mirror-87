import logging

from sqlalchemy.orm import Session
from sqlalchemy import Column, BigInteger, Text, DateTime
from fibrenest_db_models.old import Service, Base as OLDBase
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from fibrenest_db_models.postgres import ONT, SUBSCRIPTION
from tac_tasks_validation.exceptions import ValidationError, CantProceedError, ActiveSessionError


class RADACCT(OLDBase):
    __tablename__ = 'radacct'

    radacctid = Column(BigInteger, primary_key=True)
    username = Column(Text)
    realm = Column(Text)
    acctstoptime = Column(DateTime(True))


class ValidateOldOnt:
    """ Validates OLD ONT. i.e. the ONT should exists on the old system/db """

    def __init__(
            self,
            old_ont: str,
            old_db_session: Session,
            old_db_radius_session: Session,
            logger: logging.Logger
    ):
        """
        Validates OLD ONT exists on old db and that there is no active session on this ONT
        If the validation succeeds then the instance attribute `old_ont_data` will contain the OLD DB Service table
        data
        :param old_ont: ONT Serial number
        :param old_db_session: OLD DB Service table session object
        :param old_db_radius_session: OLD DB Radius table session object
        :param logger: logging object
        """

        self.old_ont = old_ont
        self.old_db_session = old_db_session
        self.old_db_radius_session = old_db_radius_session
        self.logger = logger
        self.old_ont_data = None

    def __repr__(self):
        return f'{self.__class__.__name__}(old_ont={self.old_ont})'

    def validate_old_exists(self):
        """
        Validates OLD ONT exists on old system/DB
        :return: None
        :raise ValidationError: If any validation error
        :raise ActiveSessionError: If there is an active user session
        """

        try:
            self.logger.info(f'Validating ont: {self.old_ont} exists on old system')

            self.old_ont_data: Service = self.old_db_session.query(Service).filter(Service.pon == self.old_ont).one()

            if self.old_ont_data.ont_prov_state != 'REGISTERED':
                raise ValidationError(
                    f'Validation failed for old ont: {self.old_ont}. ONT state invalid of {self.old_ont_data.ont_prov_state}'
                )

            if self.old_ont_data.cust_id \
                    and (
                    self.old_ont_data.ppp_prov_state == 'PPP_DETAILS_SET'
                    or self.old_ont_data.ppp_prov_state == 'RADIUS_RECORD_CREATED'
            ):
                self.logger.info(f'Checking that there is no active session for a customer on old ont: {self.old_ont}')

                old_radacct = self.old_db_radius_session.query(RADACCT).filter(
                    RADACCT.username == f'{self.old_ont_data.cust_id}@hsi.fibrenest.net'
                ).order_by(RADACCT.radacctid.desc()).first()

                if old_radacct and old_radacct.acctstoptime is None:
                    error_msg = f'There seems to be an online session for old ont: {self.old_ont}'
                    self.logger.error(error_msg)
                    raise ActiveSessionError(error_msg)

        except NoResultFound as no_result_error:
            raise ValidationError(f'Validation failed for old ont: {self.old_ont}. No DB record') from no_result_error
        except MultipleResultsFound as multi_result_error:
            raise ValidationError(
                f'Validation failed for old ont: {self.old_ont}. Multiple DB record') from multi_result_error

    def validate_old_not_exists(self):
        """
        Validates OLD ONT does not exists on old system/DB
        :return: None
        :raise ValidationError: If ONT exists on old system/DB
        """

        self.logger.info(f'Validating ont: {self.old_ont} does not exists on old system')
        old_ont_data: Service = self.old_db_session.query(Service).filter(Service.pon == self.old_ont).one_or_none()
        if not old_ont_data:
            self.logger.info(f'ONT: {self.old_ont} does not exists on old system')
            return
        error_msg = f'ONT: {self.old_ont} exists on old system'
        self.logger.error(error_msg)
        raise ValidationError(error_msg)


class ValidateNewOnt:
    """ Validates NEW ONT. i.e. the ONT should exists on the new system/db """

    def __init__(
            self,
            new_ont: str,
            new_db_session: Session,
            logger: logging.Logger
    ):
        """
        Validates NEW ONT exists on new db and there is not a subscription already on it.
        If the validation succeeds then the instance attribute `new_ont_data` will contain the NEW DB ONT table
        data
        :param new_ont: ONT Serial number
        :param new_db_session: NEW DB ONT table session object
        :param logger: logging object
        """

        self.new_ont = new_ont
        self.new_db_session = new_db_session
        self.logger = logger
        self.new_ont_data = None

    def __repr__(self):
        return f'{self.__class__.__name__}(new_ont={self.new_ont})'

    def validate_new_exists(self):
        """
        Validates NEW ONT exists on new system/DB
        :return: None
        :raise ValidationError: If any validation error
        """

        try:
            self.logger.info(f'Validating ont: {self.new_ont} exists on new system')

            self.new_ont_data: ONT = self.new_db_session.query(ONT).filter(ONT.sn == self.new_ont).one()

            if not self.new_ont_data.ont_registered:
                msg = f'Cannot proceed until the new ont: {self.new_ont} is registered'
                raise CantProceedError(msg)

            self.logger.info(f'Checking is there is already a subscription provided on new ont: {self.new_ont}')
            sub_on_new_ont = self.new_db_session.query(SUBSCRIPTION).filter(
                SUBSCRIPTION.ont_id == self.new_ont_data.id
            ).one_or_none()

            if sub_on_new_ont:
                error_msg = f'There is a subscription, subs_id: {sub_on_new_ont.subs_id} on new ont: {self.new_ont}'
                self.logger.error(error_msg)
                raise ValidationError(error_msg)

        except NoResultFound as no_result_error:
            raise ValidationError(f'Validation failed for new ont: {self.new_ont}. No DB record') from no_result_error
        except MultipleResultsFound as multi_result_error:
            raise ValidationError(
                f'Validation failed for new ont: {self.new_ont}. Multiple DB record') from multi_result_error

    def validate_new_not_exists(self):
        """
        Validates NEW ONT does not exists on new system/DB
        :return: None
        :raise ValidationError: If ONT exists on new system/DB
        """

        self.logger.info(f'Validating ont: {self.new_ont} does not exists on new system')
        new_ont_data: ONT = self.new_db_session.query(ONT).filter(ONT.sn == self.new_ont).one_or_none()
        if not new_ont_data:
            self.logger.info(f'ONT: {self.new_ont} does not exists on new DB')
            return
        error_msg = f'ONT: {self.new_ont} exists on new DB'
        self.logger.error(error_msg)
        raise ValidationError(error_msg)
