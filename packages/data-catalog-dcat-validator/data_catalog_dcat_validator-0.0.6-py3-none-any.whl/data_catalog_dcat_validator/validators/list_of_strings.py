from typing import Any
from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.validators.string import StringValidator


class StringOrListOfStringsValidator(Validator):
    """Validator for string or list of strings properties."""

    def validate(self, value: Any) -> None:
        """Validate input."""
        if isinstance(value, list):
            for val in value:
                StringValidator().validate(val)

        else:
            StringValidator().validate(value)
