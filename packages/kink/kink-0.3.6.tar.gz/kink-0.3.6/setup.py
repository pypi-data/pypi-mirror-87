# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kink', 'kink.errors']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'kink',
    'version': '0.3.6',
    'description': 'Dependency injection for python.',
    'long_description': '# Kink [![Build Status](https://travis-ci.org/kodemore/kink.svg?branch=master)](https://travis-ci.org/kodemore/kink) [![codecov](https://codecov.io/gh/kodemore/kink/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/kink)\nDependency injection made for python\n\n## Features\n\n- Easy to use interface\n- Extensible with custom dependency resolvers\n- Automatic dependency injection\n- Lightweight\n- Support for async with asyncio\n\n\n## Installation\n\n```\npip install kink\n```\n\n# Usage\n\n## Adding service to dependency injection container\n\nDependency container is a dict-like object, adding new service to dependency container is as \nsimple as the following example:\n\n```python\nfrom kink import di\nfrom os import getenv\n\ndi["db_name"] = getenv("DB_NAME")\ndi["db_password"] = getenv("DB_PASSWORD")\n```\n\n## Adding service factory to dependency injection container\n\nKink also supports on-demand service creation. In order to define such a service, lambda function\nshould be used: \n\n```python\nfrom kink import di\nfrom sqlite3 import connect\n\ndi["db_connection"] = lambda di: connect(di["db_name"])\n```\n\nIn this scenario connection to database will not be established until service is requested.\n\n## Requesting services fromm dependency injection container\n\n```python\nfrom kink import di\nfrom sqlite3 import connect\n\n# Setting services\ndi["db_name"] = "test_db.db"\ndi["db_connection"] = lambda di: connect(di["db_name"])\n\n\n# Getting service\n\nconnection = di["db_connection"] # will return instance of sqlite3.Connection\nassert connection == di["db_connection"] # True\n```\n\n## Autowiring dependencies\n\n```python\nfrom kink import di, inject\nfrom sqlite3 import connect, Connection\n\n\ndi["db_name"] = "test_db.db"\ndi["db_connection"] = lambda di: connect(di["db_name"])\n\n# Inject connection from di, connection is established once function is called.\n@inject\ndef get_database(db_connection: Connection):\n    ...\n\n\nconnection = get_database()\nconnection_with_passed_connection = get_database(connect("temp.db")) # will use passed connection\n```\n\n### Constructor injection\n```python\nfrom kink import inject, di\nimport MySQLdb\n\n# Set dependencies\ndi["db_host"] = "localhost"\ndi["db_name"] = "test"\ndi["db_user"] = "user"\ndi["db_password"] = "password"\ndi["db_connection"] = lambda di: MySQLdb.connect(host=di["db_host"], user=di["db_user"], passwd=di["db_password"], db=di["db_name"])\n\n@inject\nclass AbstractRepository:\n    def __init__(self, db_connection):\n        self.connection = db_connection\n\n\nclass UserRepository(AbstractRepository):\n    ...\n\n\nrepository = UserRepository()\nrepository.connection # mysql db connection is resolved and available to use.\n```\n\nWhen class is annotated by `inject` annotation it will be automatically added to the container for future use (eg autowiring).\n\n\n### Services aliasing\n\nWhen you registering service with `@inject` decorator you can attach your own alias name, please consider the following example:\n\n```python\nfrom kink import inject\nfrom typing import Protocol\n\nclass IUserRepository(Protocol):\n    ...\n\n@inject(alias=IUserRepository)\nclass UserRepository:\n    ...\n\n\nassert di[IUserRepository] == di[UserRepository] # returns true\n```\n\nFor more examples check [tests](/tests) directory\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/kink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
