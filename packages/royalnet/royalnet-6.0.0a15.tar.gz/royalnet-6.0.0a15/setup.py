# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet',
 'royalnet.alchemist',
 'royalnet.campaigns',
 'royalnet.campaigns.tests',
 'royalnet.scrolls',
 'royalnet.typing']

package_data = \
{'': ['*'], 'royalnet': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['sqlalchemy>=1.3.19,<2.0.0', 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'royalnet',
    'version': '6.0.0a15',
    'description': 'A multipurpose bot and web framework',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
