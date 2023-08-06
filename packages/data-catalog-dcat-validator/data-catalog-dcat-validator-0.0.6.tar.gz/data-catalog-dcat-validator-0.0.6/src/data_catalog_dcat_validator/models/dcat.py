"""
Deetly dcat.

Utility functions for validating dcat formated metadata
"""
from data_catalog_dcat_validator.models.base_model import BaseModel
from data_catalog_dcat_validator.validators.contactpoint import ContactValidator
from data_catalog_dcat_validator.validators.temporal import TemporalValidator
from data_catalog_dcat_validator.validators.date import DateValidator
from data_catalog_dcat_validator.validators.list_of_strings import StringOrListOfStringsValidator
from data_catalog_dcat_validator.validators.distributions import DistributionValidator
from data_catalog_dcat_validator.validators.integer import IntValidator
from data_catalog_dcat_validator.validators.string import StringValidator


class DcatModel(BaseModel):
    """DCAT model."""

    def __init__(self, metadata: dict) -> None:
        """Constructor."""
        super().__init__(metadata)

    @property
    def mandatory_fields(self):
        return []

    @property
    def recommended_fields(self):
        return []

    @property
    def optional_fields(self):
        return []

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
            "contactPoint": ContactValidator(),
            "creator": StringValidator(),
            "distribution": DistributionValidator(),
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
            "license": StringValidator(),
            "mediaType": StringValidator(),
            "modified": DateValidator(),
            "packageFormat": StringValidator(),
            "page": StringValidator(),
            "provenance": StringValidator(),
            "publisher": ContactValidator(),
            "qualifiedAttributionwasGeneratedBy": StringValidator(),
            "qualifiedRelation": StringValidator(),
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
