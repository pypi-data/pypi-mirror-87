# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vivaldi']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['vivaldi = vivaldi.cli:main']}

setup_kwargs = {
    'name': 'vivaldi',
    'version': '0.2.4',
    'description': 'Tools for working with VIVA data formats',
    'long_description': None,
    'author': 'Abhinav Tushar',
    'author_email': 'abhinav@vernacular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
