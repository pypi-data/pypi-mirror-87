# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idazen']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0', 'bleak>=0.9.1,<0.10.0', 'typer[all]>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['idazen = idazen.main:cli']}

setup_kwargs = {
    'name': 'idazen',
    'version': '0.1.2',
    'description': 'Take control over your Ikea IDÅSEN standing desk without hassle and stay ZEN 🙌.',
    'long_description': '# idazen\n\n[![Actions Status](https://github.com/zifeo/idazen/workflows/CI/badge.svg)](https://github.com/zifeo/idazen/actions)\n[![PyPI version](https://badge.fury.io/py/idazen.svg)](https://badge.fury.io/py/idazen)\n\nTake control over your Ikea IDÅSEN standing desk without hassle and stay ZEN 🙌.\n\n## Getting started\n\n```\n# pypi\npip install idazen\n\n# master\npip install --upgrade git+https://github.com/zifeo/idazen.git   \n```\n\n## Usage\n\n```\n> idazen scan\nScanning 10s...\nFound: Desk 7764 (3C9D3306-3B80-4D68-8670-AC9451083BC5)\nUse "idazen save 3C9D3306-3B80-4D68-8670-AC9451083BC5" or "idazen scan --save"\n```\n\n```\n> idazen move 78\nHeight set to 78.22\n```\n\n',
    'author': 'Teo Stocco',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zifeo/idazen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
