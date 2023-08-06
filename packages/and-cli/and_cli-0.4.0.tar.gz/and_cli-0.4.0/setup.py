# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['and_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['and = and_cli.commands:_and']}

setup_kwargs = {
    'name': 'and-cli',
    'version': '0.4.0',
    'description': 'Simple CLI for COMP4128',
    'long_description': None,
    'author': 'Felix Lonergan',
    'author_email': 'felix.lonergan@gmail.com',
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
