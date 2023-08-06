# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaea',
 'gaea.config',
 'gaea.constants',
 'gaea.database',
 'gaea.database.utils',
 'gaea.errors',
 'gaea.helpers',
 'gaea.log',
 'gaea.models',
 'gaea.models.utils',
 'gaea.rbmq',
 'gaea.rbmq.utils',
 'gaea.redis',
 'gaea.webapp']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'dynaconf>=3.0.0,<4.0.0',
 'fastapi>=0.61.0,<0.62.0',
 'pika>=1.1.0,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'sqlalchemy>=1.3.18,<2.0.0',
 'uvicorn>=0.11.8,<0.12.0']

setup_kwargs = {
    'name': 'gaea',
    'version': '0.1.19',
    'description': '',
    'long_description': None,
    'author': 'rarnal',
    'author_email': 'arnal.romain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
