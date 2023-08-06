# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_generator']

package_data = \
{'': ['*'], 'sql_generator': ['resources/*']}

install_requires = \
['argon2-cffi>=20.1.0,<21.0.0', 'psycopg2>=2.8.6,<3.0.0', 'toposort>=1.5,<2.0']

setup_kwargs = {
    'name': 'sql-generator',
    'version': '0.1.0',
    'description': 'SQL Generator for Postgresql-backed systems',
    'long_description': None,
    'author': 'ilevn',
    'author_email': 'nilsntth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
