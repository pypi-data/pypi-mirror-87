# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biip', 'biip.gs1', 'biip.gtin']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<4.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 'money': ['py-moneyed>=0.8.0,<0.9.0']}

setup_kwargs = {
    'name': 'biip',
    'version': '0.6.1',
    'description': 'Biip interprets the data in barcodes.',
    'long_description': '# &#x1F4E6; Biip\n\n_Biip interprets the data in barcodes._\n\n[![Tests](https://img.shields.io/github/workflow/status/jodal/biip/Tests)](https://github.com/jodal/biip/actions?workflow=Tests)\n[![Docs](https://img.shields.io/readthedocs/biip)](https://biip.readthedocs.io/en/latest/)\n[![Coverage](https://img.shields.io/codecov/c/gh/jodal/biip)](https://codecov.io/gh/jodal/biip)\n[![PyPI](https://img.shields.io/pypi/v/biip)](https://pypi.org/project/biip/)\n\n---\n\nBiip is a Python library for making sense of the data in barcodes.\n\nThe library can interpret the following formats:\n\n- GTIN-8, GTIN-12, GTIN-13, and GTIN-14 numbers,\n  commonly found in EAN-8, EAN-13, UPC-A, UPC-E, and ITF-14 barcodes.\n\n- GS1 AI element strings,\n  commonly found in GS1-128 barcodes.\n\nFor a quickstart guide and a complete API reference,\nsee the [documentation](https://biip.readthedocs.io/).\n\n## Installation\n\nBiip requires Python 3.6 or newer.\n\nBiip is available from [PyPI](https://pypi.org/project/biip/):\n\n```\npython3 -m pip install biip\n```\n\nOptionally, with the help of `py-moneyed`, Biip can convert amounts with\ncurrency information to `moneyed.Money` objects.\nTo install Biip with `py-moneyed`, run:\n\n```\npython3 -m pip install "biip[money]"\n```\n\n## Development status\n\nAll planned features have been implemented.\nWhen the library has seen some extended production usage,\nwe should be ready to make a 1.0 release.\n\nPlease open an issue if you have and barcode parsing related needs that are not covered.\n\n## Features\n\n- GS1 (multiple Element Strings with Application Identifiers)\n  - [x] Recognize all specified Application Identifiers.\n  - [x] Recognize allocating GS1 Member Organization from the GS1 Company Prefix.\n  - [x] Parse fixed-length Element Strings.\n  - [x] Parse variable-length Element Strings.\n    - [x] Support configuring the separation character.\n  - [x] Parse AI `00` as SSCC.\n  - [x] Parse AI `01` and `02` as GTIN.\n  - [x] Parse dates into `datetime.date` values.\n    - [x] Interpret the year to be within -49/+50 years from today.\n    - [x] Interpret dates with day "00" as the last day of the month.\n  - [x] Parse variable measurement fields into `Decimal` values.\n  - [x] Parse discount percentage into `Decimal` values.\n  - [x] Parse amounts into `Decimal` values.\n    - [x] Additionally, if py-moneyed is installed,\n          parse amounts with currency into `Money` values.\n  - [x] Encode as Human Readable Interpretation (HRI),\n        e.g. with parenthesis around the AI numbers.\n  - [x] Easy lookup of parsed Element Strings by:\n    - [x] Application Identifier (AI) prefix\n    - [x] Part of AI\'s data title\n- GTIN (Global Trade Item Number)\n  - [x] Parse GTIN-8, e.g. from EAN-8 barcodes.\n  - [x] Parse GTIN-12, e.g. from UPC-A and UPC-E barcodes.\n  - [x] Parse GTIN-13, e.g. from EAN-13 barcodes.\n  - [x] Parse GTIN-14, e.g. from ITF-14 and GS1-128 barcodes.\n  - [x] Extract and validate check digit.\n  - [x] Extract GS1 Prefix.\n  - [x] Extract packaging level digit from GTIN-14.\n  - [x] Encode GTIN-8 as GTIN-12/13/14.\n  - [x] Encode GTIN-12 as GTIN-13/14.\n  - [x] Encode GTIN-13 as GTIN-14.\n- RCN (Restricted Circulation Numbers), a subset of GTINs\n  - [x] Classification of RCN usage to either a geographical region or a company.\n  - [x] Parsing of variable measurements (price/weight) into `Decimal`\n        values.\n  - [x] Parsing of price values into `Money` values if `py-moneyed` is\n        installed and the region\'s RCN parsing rules specifies a currency.\n  - [x] Baltics: Parsing of weight.\n  - [x] Great Britain: Parsing of price, including validation of price check digit.\n  - [x] Norway: Parsing of weight and price.\n  - [x] Sweden: Parsing of weight and price.\n  - [x] Encode RCN with the variable measure part zeroed out,\n        to help looking up the correct trade item.\n- SSCC (Serial Shipping Container Code)\n  - [x] Validate check digit.\n  - [x] Encode for human consumption, with the logical groups separated by whitespace.\n- Symbology Identifers, e.g. `]EO`\n  - [x] Recognize all specified Symbology Identifier code characters.\n  - [x] Strip Symbology Identifers before parsing the remainder.\n  - [x] Use Symbology Identifers when automatically selecting what parser to use.\n\n## License\n\nBiip is copyright 2020 Stein Magnus Jodal and contributors.\nBiip is licensed under the\n[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'Stein Magnus Jodal',
    'author_email': 'stein.magnus@jodal.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jodal/biip',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
