from textwrap import indent

from data_catalog_dcat_validator.validators.publisher import PublisherValidator
from data_catalog_dcat_validator.validators.date import DateValidator
from data_catalog_dcat_validator.validators.list_of_strings import StringOrListOfStringsValidator
from data_catalog_dcat_validator.validators.contactpoint import ContactValidator
from data_catalog_dcat_validator.models.base_model import BaseModel


class DcatResourceModel(BaseModel):

    @property
    def mandatory_fields(self):
        return ['title', 'description']

    @property
    def recommended_fields(self):
        return ['contactPoint',
                'issued',
                'modified',
                'creator',
                'language',
                'publisher',
                'identifier',
                'license',
                'rights',
                'keyword',
                'theme']

    @property
    def optional_fields(self):
        return ['accessRights',
                'conformsTo',
                'type',
                'relation',
                'qualifiedRelation',
                'landingPage',
                'qualifiedAttribution',
                'hasPolicy',
                'isReferencedBy']

    @property
    def validators(self):
        return {
            'contactPoint': ContactValidator(),
            'issued': DateValidator(),
            'modified': DateValidator(),
            'language': StringOrListOfStringsValidator(),
            'publisher': PublisherValidator(),
            'keyword': StringOrListOfStringsValidator()
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
