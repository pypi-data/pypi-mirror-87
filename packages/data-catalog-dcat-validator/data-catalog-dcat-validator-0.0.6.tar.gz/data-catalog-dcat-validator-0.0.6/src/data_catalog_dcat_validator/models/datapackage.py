from textwrap import indent

from data_catalog_dcat_validator.validators.publisher import PublisherValidator
from data_catalog_dcat_validator.validators.temporal import TemporalValidator
from data_catalog_dcat_validator.validators.date import DateValidator
from data_catalog_dcat_validator.validators.list_of_strings import StringOrListOfStringsValidator
from data_catalog_dcat_validator.validators.contactpoint import ContactValidator
from data_catalog_dcat_validator.validators.integer import IntValidator
from data_catalog_dcat_validator.models.base_model import BaseModel
from data_catalog_dcat_validator.validators.string import StringValidator


class DataPackageModel(BaseModel):
    """Model for dataverk datapackage."""

    @property
    def mandatory_fields(self):
        return ["title", "bucket"]

    @property
    def recommended_fields(self):
        return [
            "author",
            "category",
            "contactpoint",
            "description",
            "format",
            "keyword",
            "license",
            "project",
            "publisher",
            "readme",
            "spatial",
            "temporal",
            "theme",

        ]

    @property
    def optional_fields(self):
        return [
            "identifier",
            "sample",
            "versionNotes",
            "landingPage",
            "spatialResolutionInMeters",
            "temporalResolution",
            "qualifiedRelation",
            "accessRights",
            "accrualPeriodicity",
            "conformsTo",
            "creator",
            "hasVersion",
            "isReferencedBy",
            "isVersionOf",
            "identifier",
            "issued",
            "language",
            "modified",
            "notebook",
            "repo",
            "provenance",
            "relation",
            "source",
            "spatial",
            "store",
            "type",
            "page",
            "versionInfo",
            "qualifiedAttribution",
            "wasGeneratedBy"
        ]

    @property
    def validators(self):
        return {
            "accessRights": StringValidator(),
            "accessService": StringValidator(),
            "accessURL": StringValidator(),
            "accrualPeriodicity": StringValidator(),
            "availability": StringValidator(),
            "byteSize": IntValidator(),
            "checksum": StringValidator(),
            "compressFormat": StringValidator(),
            "conformsTo": StringValidator(),
            "contactpoint": ContactValidator(),
            "creator": StringValidator(),
            "downloadURL": StringValidator(),
            "format": StringOrListOfStringsValidator(),
            "hasPolicy": StringValidator(),
            "hasVersion": StringValidator(),
            "identifier": StringValidator(),
            "isReferencedBy": StringValidator(),
            "isVersionOf": StringValidator(),
            "issued": DateValidator(),
            "keyword": StringOrListOfStringsValidator(),
            "landingPage": StringValidator(),
            "language": StringOrListOfStringsValidator(),
            "license": PublisherValidator(),
            "mediaType": StringValidator(),
            "modified": DateValidator(),
            "packageFormat": StringValidator(),
            "page": StringValidator(),
            "provenance": StringValidator(),
            "publisher": PublisherValidator(),
            "qualifiedAttributionwasGeneratedBy": StringValidator(),
            "qualifiedRelation": StringValidator(),
            "readme": StringValidator(),
            "relation": StringValidator(),
            "rights": StringValidator(),
            "sample": StringValidator(),
            "source": StringValidator(),
            "spatial": StringValidator(),
            "spatialResolutionInMeters": IntValidator(),
            "status": StringValidator(),
            "temporal": TemporalValidator(),
            "temporalResolution": StringValidator(),
            "theme": StringOrListOfStringsValidator(),
            "type": StringValidator(),
            "versionInfo": StringValidator(),
            "versionNotes": StringValidator(),
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
