# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['network_importer',
 'network_importer.adapters',
 'network_importer.adapters.netbox_api',
 'network_importer.adapters.network_importer',
 'network_importer.drivers',
 'network_importer.processors']

package_data = \
{'': ['*'], 'network_importer': ['templates/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'diffsync>=1.0.0,<2.0.0',
 'genie.metaparser>=19.12,<20.0',
 'genie>=20.9,<21.0',
 'jsonschema>=3.2.0,<4.0.0',
 'netmiko>=3.3.2,<4.0.0',
 'nornir>=2.4,<3.0',
 'ntc-templates>=1.6.0,<2.0.0',
 'pyats>=20.9,<21.0',
 'pybatfish>=2020.8.11,<2021.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'pynetbox>=5.0,<6.0',
 'structlog>=20.1.0,<21.0.0',
 'termcolor>=1.1,<2.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['network-importer = network_importer.cli:main']}

setup_kwargs = {
    'name': 'network-importer',
    'version': '2.0.0b2',
    'description': 'Network Importer tool to import an existing network into a Database / Source Of Truth',
    'long_description': None,
    'author': 'Damien Garros',
    'author_email': 'dgarros@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
