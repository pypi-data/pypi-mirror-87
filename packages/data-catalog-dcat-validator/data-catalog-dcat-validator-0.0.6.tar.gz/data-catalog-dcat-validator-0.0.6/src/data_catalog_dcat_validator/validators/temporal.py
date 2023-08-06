from collections import defaultdict

from data_catalog_dcat_validator.models.temporal import TemporalModel
from data_catalog_dcat_validator.validators.base import Validator


class TemporalValidator(Validator):
    hint = "Dict"

    def validate(self, value: dict) -> defaultdict:
        return TemporalModel(value).validate()
