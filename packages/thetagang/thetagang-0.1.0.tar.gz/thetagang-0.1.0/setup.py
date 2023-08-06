# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thetagang']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'ib_insync>=0.9.64,<0.10.0',
 'pandas>=1.1.4,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['thetagang = thetagang.entry:cli',
                     'vscode = vscode:vscode']}

setup_kwargs = {
    'name': 'thetagang',
    'version': '0.1.0',
    'description': 'ThetaGang is an IBKR bot for getting money',
    'long_description': None,
    'author': 'Brenden Matthews',
    'author_email': 'brenden@brndn.io',
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
