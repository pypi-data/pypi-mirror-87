# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mldl',
 'mldl.cli',
 'mldl.cli.tests',
 'mldl.datarepo',
 'mldl.datarepo.mappers',
 'mldl.datarepo.storage',
 'mldl.datarepo.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0', 'azure-storage-blob>=12.5,<13.0']

entry_points = \
{'console_scripts': ['mldl = mldl.__main__:main']}

setup_kwargs = {
    'name': 'mldl',
    'version': '0.0.6',
    'description': 'Machine Learning Data Lineage tool (MLDL)',
    'long_description': None,
    'author': 'Vlad Kolesnikov',
    'author_email': None,
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
