# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_postgres']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.8.6,<3.0.0']

setup_kwargs = {
    'name': 'test-postgres',
    'version': '0.1.2',
    'description': 'Context for PostgreSQL database testing',
    'long_description': None,
    'author': 'Yevhen Shymotiuk',
    'author_email': 'yevhenshymotiuk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yevhenshymotiuk/test_postgres',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
