# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cmdlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cmdlib',
    'version': '0.7.0',
    'description': '',
    'long_description': None,
    'author': 'Xavier Martinez-Hidalgo',
    'author_email': 'xavier@martinezhidalgo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
