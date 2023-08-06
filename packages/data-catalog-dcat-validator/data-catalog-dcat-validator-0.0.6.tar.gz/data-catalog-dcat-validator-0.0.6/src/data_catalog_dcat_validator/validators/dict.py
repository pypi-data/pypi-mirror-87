from typing import Any

from data_catalog_dcat_validator.errors.exceptions import InvalidTypeException
from data_catalog_dcat_validator.validators.base import Validator


class DictValidator(Validator):
    """Dict validator"""

    hint = "dict"

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise InvalidTypeException(value, self.hint, type(value).__name__)
