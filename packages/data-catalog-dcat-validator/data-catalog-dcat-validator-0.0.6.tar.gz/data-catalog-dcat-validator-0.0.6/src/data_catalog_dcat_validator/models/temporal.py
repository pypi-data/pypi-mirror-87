from data_catalog_dcat_validator.validators.date import DateValidator
from data_catalog_dcat_validator.models.base_model import BaseModel


class TemporalModel(BaseModel):
    def __int__(self, contact_point: dict):
        super().__init__(contact_point)

    @property
    def mandatory_fields(self):
        return ['from', 'to']

    @property
    def recommended_fields(self):
        return []

    @property
    def optional_fields(self):
        return []

    @property
    def validators(self):
        return {"from": DateValidator(),
                "to": DateValidator()}
