from data_catalog_dcat_validator.validators.date import StringValidator
from data_catalog_dcat_validator.models.base_model import BaseModel


class PublisherModel(BaseModel):
    def __int__(self, publisher: dict):
        super().__init__(publisher)

    @property
    def mandatory_fields(self):
        return ['name', 'url']

    @property
    def recommended_fields(self):
        return []

    @property
    def optional_fields(self):
        return []

    @property
    def validators(self):
        return {"from": StringValidator(),
                "to": StringValidator()}
