# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cogwatch']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.5,<2.0', 'watchgod==0.6']

setup_kwargs = {
    'name': 'cogwatch',
    'version': '1.1.6',
    'description': 'Automatic hot-reloading for your discord.py command files.',
    'long_description': None,
    'author': 'Rob Wagner',
    'author_email': '13954303+robertwayne@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
