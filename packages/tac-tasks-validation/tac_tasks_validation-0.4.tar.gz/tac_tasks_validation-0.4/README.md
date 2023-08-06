# tac_tasks_validation
Performs validation for tasks performed by TAC. Involves validating the data input like ONTs

## Usage
Import the various validations from `tac_tasks_validation`
```python
from tac_tasks_validation import OltToNewValidation
validate = OltToNewValidation(
            old_ont='some_ont_sn',
            new_ont='another_ont_sn',
            logger=logger,  # logging.Logger object
            old_db_session=old_db_session,  # sqlalchemy.orm.Session object
            old_db_radius_session=old_db_radius_session,  # sqlalchemy.orm.Session object
            new_db_session=new_db_session  # sqlalchemy.orm.Session object
        )
validate.validate_old_to_new_swap()
```



