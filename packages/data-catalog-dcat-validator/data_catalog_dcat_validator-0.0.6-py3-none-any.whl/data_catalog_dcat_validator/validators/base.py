from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """Validator base class."""

    hint = "Not implemented validator"

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Validate method in base class."""
        raise NotImplementedError()
