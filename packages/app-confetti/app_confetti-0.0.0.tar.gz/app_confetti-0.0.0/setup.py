# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app_confetti', 'app_confetti.settings']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.49,<2.0.0',
 'ec2-metadata>=2.2.0,<3.0.0',
 'environ-config>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'app-confetti',
    'version': '0.0.0',
    'description': 'Environment application configuration',
    'long_description': '# Configuration Fetcher v0.0.0\n\nCommon code for interacting with dev environs and for deployed AWS environs.\n',
    'author': 'Daniel Edgecombe',
    'author_email': 'edgy.edgemond@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EdgyEdgemond/app-confetti/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
