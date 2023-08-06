from data_catalog_dcat_validator.validators.string import StringValidator
from data_catalog_dcat_validator.validators.email import EmailValidator
from data_catalog_dcat_validator.models.base_model import BaseModel


class ContactPointModel(BaseModel):
    def __int__(self, contact_point: dict):
        super().__init__(contact_point)

    @property
    def mandatory_fields(self):
        return ['name', 'email']

    @property
    def recommended_fields(self):
        return []

    @property
    def optional_fields(self):
        return []

    @property
    def validators(self):
        return {"name": StringValidator(),
                "email": EmailValidator()}
