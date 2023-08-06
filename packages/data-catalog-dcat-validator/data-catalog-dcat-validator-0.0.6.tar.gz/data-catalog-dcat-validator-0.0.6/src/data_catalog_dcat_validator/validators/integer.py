from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException


class IntValidator(Validator):
    """Validator for integer properties."""

    hint = "int"

    def validate(self, value: int) -> None:
        """Validate input."""

        if not isinstance(value, int):
            raise InvalidTypeException(value, self.hint, type(value).__name__)
