import re

from data_catalog_dcat_validator.errors.exceptions import InvalidValueException
from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.validators.string import StringValidator


class EmailValidator(Validator):
    """Validator for string with email properties"""

    hint = "str formatted as 'mail@example.com'"

    def validate(self, value: str) -> None:
        """Validate input"""

        # Raises InvalidTypeException if not string
        StringValidator().validate(value)

        if not re.match(r"[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+", value):
            raise InvalidValueException(value, self.hint)
