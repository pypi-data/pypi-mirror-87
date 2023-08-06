# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pagebits']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'pagebits',
    'version': '0.1.0',
    'description': 'Static fact storage and site generator',
    'long_description': None,
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
