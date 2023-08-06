from data_catalog_dcat_validator.models.distribution import DistributionModel

from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException
from data_catalog_dcat_validator.validators.base import Validator


class DistributionValidator(Validator):
    """Validator for Distribution properties."""

    hint = "Distribution validator"

    def validate(self, value: list) -> dict:
        """Validate input."""
        if not isinstance(value, list):
            raise InvalidTypeException(value, list, type(value).__name__)

        errors = {}
        for i in range(len(value)):
            errors[i] = DistributionModel(value[i]).validate()

        return errors
