# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['website_checker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.0,<3.0.0', 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'console_scripts': ['check = website_checker.cli:cli']}

setup_kwargs = {
    'name': 'website-checker',
    'version': '0.1.1a2',
    'description': 'A simple python application for running checks against websites.',
    'long_description': None,
    'author': 'aidanmelen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
