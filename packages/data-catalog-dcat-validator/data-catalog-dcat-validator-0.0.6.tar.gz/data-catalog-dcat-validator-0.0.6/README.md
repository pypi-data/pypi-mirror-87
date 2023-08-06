# data-catalog-dcat-validator

## Example use
````python
from data_catalog_dcat_validator.models.dataset import DatasetModel

metadata = {
    "title": "Zimbabwe Regional Geochemical Survey.",
    "description": "During the period 1982-86 a team of geologists ...",
    "identifier": "9df8df51-63db-37a8-e044-0003ba9b0d98",
    "landingPage": "http://some.source.url.com",
    "issued": "2012-05-10",
    "modified": "2012-05-10T21:04",
    "language": ["en", "es", "ca"],
    "keyword": [
        "exploration",
        "geochemical-exploration",
        "geochemical-maps",
        "geochemistry",
        "geology",
        "nercddc",
        "regional-geology",
    ],
    "publisher": {"name": "Geological Society", "mbox": "info@gs.org"},
    "distribution": [
        {
            "accessURL": "http://www.bgs.ac.uk/gbase/geochemcd/home.html",
            "byteSize": 235,
            "description": "Resource locator",
            "format": "text/html",
            "title": "",
        }
    ],
}

validator = DatasetModel(metadata)
validator.validate()
validator.error_report()
````
Output:
````json
{ "Missing recommended props(s)": [ "contactPoint",
                                    "spatial",
                                    "temporal",
                                    "theme"],
  "publisher": [ { "Missing mandatory props(s)": ["email"],
                   "Prop(s) not in DCAT schema": ["mbox"]}]}
````