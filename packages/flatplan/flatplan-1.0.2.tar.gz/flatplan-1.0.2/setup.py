# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flatplan']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4,<0.5', 'coloredlogs>=14.0,<15.0', 'fire>=0.3,<0.4']

entry_points = \
{'console_scripts': ['flatplan = flatplan:main']}

setup_kwargs = {
    'name': 'flatplan',
    'version': '1.0.2',
    'description': 'Flatplan is a tool that groups all resources and providers specified in a Terraform plan file into a list',
    'long_description': None,
    'author': 'Egon Braun',
    'author_email': 'egon@mundoalem.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
