# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink_data_generation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pandas>=1.1.4,<2.0.0', 'splink>=0.2.5,<0.3.0']

setup_kwargs = {
    'name': 'splink-data-generation',
    'version': '0.1.0',
    'description': 'Generate synthetic data with a specified data generating process',
    'long_description': None,
    'author': 'Robin Linacre',
    'author_email': 'robinlinacre@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
