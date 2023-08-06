from enum import Enum


class ErrorType(str, Enum):
    ERROR_OTHER = "Could not be validated"
    ERROR_INVALID_VALUE = "Invalid value(s)"
    ERROR_MISSING_PROPERTY = "Missing mandatory prop(s)"
    ERROR_VALIDATION = "Could not be validated"
    ERROR_INVALID_PROPERTY = "Prop(s) not in DCAT schema"
    WARNING_MISSING_RECOMMENDED_PROPERTY = "Missing recommended prop(s)"


class BaseError(Exception):
    """ Base class for errors """


class BaseWarning(Exception):
    """ Base class for warnings """


class InvalidValueException(BaseError):
    """
    Not valid value
    """
    def __init__(self, value, format):
        self.value = value
        self.format = format
        self.code = ErrorType.ERROR_INVALID_VALUE.value


class InvalidTypeException(BaseError):
    """
    Not valid type
    """

    def __init__(self, value, expected_type, got_type):
        self.code = ErrorType.ERROR_VALIDATION.value
        self.value = value
        self.expected_type = expected_type
        self.got_type = got_type


class ErrorInvalidPropertyException(BaseError):
    """
    Not valid dcat property
    """
    def __init__(self, values):
        self.code = ErrorType.ERROR_INVALID_PROPERTY.value
        self.values = values


class ErrorMissingPropertyException(BaseError):
    """
    Missing fields
    """
    def __init__(self, values):
        self.code = ErrorType.ERROR_MISSING_PROPERTY.value
        self.values = values


class WarningMissingRecommendedPropertyException(BaseWarning):
    """
    Missing fields
    """
    def __init__(self, values):
        self.code = ErrorType.WARNING_MISSING_RECOMMENDED_PROPERTY.value
        self.values = values
