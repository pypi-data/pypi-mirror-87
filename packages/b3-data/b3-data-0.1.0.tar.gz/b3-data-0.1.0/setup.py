# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b3_data']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['b3-data = b3_data.main:cli']}

setup_kwargs = {
    'name': 'b3-data',
    'version': '0.1.0',
    'description': 'Download quote data from b3.com.br',
    'long_description': None,
    'author': 'Wesley Batista',
    'author_email': None,
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
