# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sneact']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sneact',
    'version': '0.0.3',
    'description': 'Sneact is a python library for building user interfaces',
    'long_description': '# Sneact',
    'author': 'Kiselev Nikolay',
    'author_email': 'ceo@machineand.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://machineand.me/sneact?f=pypi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
