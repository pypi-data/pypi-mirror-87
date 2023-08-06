# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fritzbox_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'fritzbox-api',
    'version': '0.1.0',
    'description': 'REST API implementation for the Fritzbox router',
    'long_description': None,
    'author': 'Oskar Herz',
    'author_email': 'herz@gmail.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
