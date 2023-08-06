from typing import Dict
from textwrap import indent

from data_catalog_dcat_validator.models.base_model import BaseModel
from data_catalog_dcat_validator.validators.integer import IntValidator
from data_catalog_dcat_validator.validators.bool import BoolValidator


class DistributionModel(BaseModel):
    """DCAT Distribution."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(DistributionModel, self).__init__(metadata)

    @property
    def mandatory_fields(self):
        return ["accessURL"]

    @property
    def recommended_fields(self):
        return ["availability", "description", "format", "license"]

    @property
    def optional_fields(self):
        return [
            "status",
            "accessService",
            "byteSize",
            "compressFormat",
            "downloadURL",
            "mediaType",
            "packageFormat",
            "spatialResolutionInMeters",
            "temporalResolution",
            "conformsTo",
            "issued",
            "language",
            "modified",
            "rights",
            "title",
            "page",
            "hasPolicy",
            "checksum",
        ]

    @property
    def validators(self):
        return {
            "byteSize": IntValidator(),
            "compressed": BoolValidator()
        }

    def error_report(self):
        print(self.parse_errors(self.errors))

    def parse_errors(self, errors: dict, ind: int = 0, out: str = "") -> str:
        for key, value in errors.items():
            out += indent(f"- {key}:", "\t" * ind)
            if isinstance(value, dict):
                out += '\n' + self.parse_errors(value, ind + 1)
            else:
                out += indent(f"{value} \n", " ")

        return out
