from abc import ABC, abstractmethod
from typing import List, Any


from data_catalog_dcat_validator.errors.exceptions import InvalidValueException, ErrorInvalidPropertyException, \
    WarningMissingRecommendedPropertyException, InvalidTypeException, ErrorMissingPropertyException, ErrorType
from data_catalog_dcat_validator.validators.string import StringValidator
from data_catalog_dcat_validator.validators.base import Validator


class BaseModel(ABC):
    """
    A model has to have more than one field.'
    """
    def __init__(self, metadata: dict):
        self.metadata = metadata
        self.errors = {}

    @property
    @abstractmethod
    def mandatory_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def recommended_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def optional_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def validators(self):
        raise NotImplementedError()

    def get_validator(self, key: Any) -> Validator:
        """Get validator for key. If key not does not exist then StringValidator"""

        validator = self.validators.get(key, StringValidator())

        return validator

    def get_properties(self) -> List:
        """Get list of all properties."""
        return [*self.mandatory_fields, *self.recommended_fields, *self.optional_fields]

    def _invalid_fields(self):
        """Checks if properties in DCAT schema"""
        non_dcat_fields = [field for field in self.metadata.keys() if field not in self.get_properties()]
        if non_dcat_fields:
            raise ErrorInvalidPropertyException(non_dcat_fields)

    def _check_mandatory_fields(self):
        """Checks if mandatory properties in metadata"""
        missing_mandatory_fields = [field for field in self.mandatory_fields if field not in self.metadata.keys()]
        if missing_mandatory_fields:
            raise ErrorMissingPropertyException(missing_mandatory_fields)

    def _check_recommended_fields(self):
        """Checks if recommended properties in metadata"""
        missing_recommended_fields = [field for field in self.recommended_fields if field not in self.metadata.keys()]
        if missing_recommended_fields:
            raise WarningMissingRecommendedPropertyException(missing_recommended_fields)

    def validate_content(self) -> None:
        """Check if mandatory and recommended properties are included."""

        try:
            self._check_mandatory_fields()
        except ErrorMissingPropertyException as err:
            for field in err.values:
                self.errors.setdefault(err.code, []).append(field)

        try:
            self._check_recommended_fields()
        except WarningMissingRecommendedPropertyException as err:
            for field in err.values:
                self.errors.setdefault(err.code, []).append(field)

        try:
            self._invalid_fields()
        except ErrorInvalidPropertyException as err:
            for field in err.values:
                self.errors.setdefault(err.code, []).append(field)

    def validate(self):
        """Validate model"""

        self.validate_content()

        for field, val in self.metadata.items():
            try:
                field_errors = self.get_validator(field).validate(val)
                if field_errors:
                    self.errors.setdefault(field, field_errors)
            except InvalidTypeException as err:
                self.errors.setdefault(field, {"expected": err.expected_type, "got": err.got_type})
            except InvalidValueException as err:
                self.errors.setdefault(field, {"expected": err.format, "got": err.value})

        return self.errors
