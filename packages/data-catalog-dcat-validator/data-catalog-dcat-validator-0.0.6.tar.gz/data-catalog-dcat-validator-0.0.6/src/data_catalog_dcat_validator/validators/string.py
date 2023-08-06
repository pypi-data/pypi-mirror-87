from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException


class StringValidator(Validator):
    """Validator for string properties."""

    hint = "str"

    def validate(self, value: str) -> None:
        """Validate input."""
        if not isinstance(value, str):
            raise InvalidTypeException(value, self.hint, type(value).__name__)
