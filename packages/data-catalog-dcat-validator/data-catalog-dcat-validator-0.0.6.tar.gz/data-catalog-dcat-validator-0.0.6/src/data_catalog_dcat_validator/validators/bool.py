from data_catalog_dcat_validator.validators.base import Validator
from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException


class BoolValidator(Validator):
    """Validator for integer properties."""

    hint = "bool"

    def validate(self, value: int) -> None:
        """Validate input."""

        if not isinstance(value, bool):
            raise InvalidTypeException(value, self.hint, type(value).__name__)
