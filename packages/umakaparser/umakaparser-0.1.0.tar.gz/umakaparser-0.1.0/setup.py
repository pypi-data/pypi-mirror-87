# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umakaparser', 'umakaparser.scripts', 'umakaparser.scripts.services']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'isodate>=0.6.0,<0.7.0',
 'pyparsing>=2.4,<3.0',
 'rdflib>=4.2,<5.0',
 'tqdm>=4.52.0,<5.0.0']

entry_points = \
{'console_scripts': ['umakaparser = umakaparser.services:cmd']}

setup_kwargs = {
    'name': 'umakaparser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DBCLS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://umaka-viewer.dbcls.jp/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
