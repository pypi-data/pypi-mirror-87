from isodate import parse_date, parse_datetime
from isodate.isoerror import ISO8601Error
from typing import Callable

from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.validators.string import StringValidator
from data_catalog_dcat_validator.errors.exceptions import InvalidValueException


class DateValidator(Validator):
    """Validator for date or datetime properties."""

    hint = "ISO date or datetime"

    def validate(self, value: str) -> None:
        """Validate input."""

        StringValidator().validate(value)

        try:
            self.parse_str(parse_date, value)
        except InvalidValueException:
            self.parse_str(parse_datetime, value)

    def parse_str(self, parse_function: Callable, value: str):
        try:
            parse_function(value)
        except (ValueError, ISO8601Error):
            raise InvalidValueException(value, self.hint)
