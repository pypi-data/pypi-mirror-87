from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException
from data_catalog_dcat_validator.models.publisher import PublisherModel
from data_catalog_dcat_validator.validators.base import Validator


class PublisherValidator(Validator):
    """Validator for contact dict properties."""

    hint = "dict"

    def validate(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise InvalidTypeException(value, self.hint, type(value).__name__)
        else:
            return PublisherModel(value).validate()
