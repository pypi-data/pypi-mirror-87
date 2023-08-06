# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simdak', 'simdak.paud', 'simdak.template']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'openpyxl>=3.0.5,<4.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'simdak',
    'version': '0.8.1',
    'description': 'Importer-exporter data Simdak Kemdikbud',
    'long_description': '# Simdak\n\n[![simdak - PyPi](https://img.shields.io/pypi/v/simdak)](https://pypi.org/project/simdak/)\n[![Tutorial](https://img.shields.io/badge/Tutorial-Penggunaan-informational)](docs/README.md)\n[![Group Telegram](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/simdak_paud)\n\nPython client module Simdak Kemdikbud\n\n## Fitur\n\nFitur export dan import data _Simdak Paud-Dikmas_.\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Kemdikbud](https://kemdikbud.go.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri._\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dapodix/simdak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
