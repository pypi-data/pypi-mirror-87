# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nikw']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'nikw',
    'version': '0.0.0',
    'description': 'Nikw, a game solver.',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
