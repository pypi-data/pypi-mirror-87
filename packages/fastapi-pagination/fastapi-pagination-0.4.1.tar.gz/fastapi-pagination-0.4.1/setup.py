# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_pagination', 'fastapi_pagination.ext']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.2,<0.62.0', 'pydantic>=1.7.2,<2.0.0']

extras_require = \
{'all': ['gino[starlette]>=1.0.1,<2.0.0',
         'SQLAlchemy>=1.3.20,<2.0.0',
         'sqlalchemy-stubs>=0.3,<0.4',
         'databases[mysql,sqlite,postgresql]>=0.4.0,<0.5.0',
         'orm>=0.1.5,<0.2.0',
         'tortoise-orm[aiosqlite,asyncpg,aiomysql]>=0.16.18,<0.17.0'],
 'databases': ['databases[mysql,sqlite,postgresql]>=0.4.0,<0.5.0'],
 'gino': ['gino[starlette]>=1.0.1,<2.0.0',
          'SQLAlchemy>=1.3.20,<2.0.0',
          'sqlalchemy-stubs>=0.3,<0.4'],
 'orm': ['databases[mysql,sqlite,postgresql]>=0.4.0,<0.5.0',
         'orm>=0.1.5,<0.2.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.20,<2.0.0', 'sqlalchemy-stubs>=0.3,<0.4'],
 'tortoise': ['tortoise-orm[aiosqlite,asyncpg,aiomysql]>=0.16.18,<0.17.0']}

setup_kwargs = {
    'name': 'fastapi-pagination',
    'version': '0.4.1',
    'description': 'FastAPI pagination',
    'long_description': "# FastAPI Pagination\n\n## Installation\n\n```bash\n# Basic version\npip install fastapi-pagination\n\n# All available integrations\npip install fastapi-pagination[all]\n```\n\nAvailable integrations:\n* [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)\n* [gino](https://github.com/python-gino/gino)\n* [databases](https://github.com/encode/databases)\n* [orm](https://github.com/encode/orm)\n* [tortoise](https://github.com/tortoise/tortoise-orm)\n\n\n## Example\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom pydantic import BaseModel\n\nfrom fastapi_pagination import PaginationParams, Page\nfrom fastapi_pagination.paginator import paginate\n\napp = FastAPI()\n\nclass User(BaseModel):\n    name: str\n    surname: str\n\nusers = [\n    User(name='Yurii', surname='Karabas'),\n    # ...\n]\n\n@app.get('/users', response_model=Page[User])\nasync def get_users(params: PaginationParams = Depends()):\n    return paginate(users, params)\n```\n\n## Example using implicit params\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom pydantic import BaseModel\n\nfrom fastapi_pagination import Page, pagination_params\nfrom fastapi_pagination.paginator import paginate\n\napp = FastAPI()\n\nclass User(BaseModel):\n    name: str\n    surname: str\n\nusers = [\n    User(name='Yurii', surname='Karabas'),\n    # ...\n]\n\n@app.get('/users', response_model=Page[User], dependencies=[Depends(pagination_params)])\nasync def get_users():\n    return paginate(users)\n```\n",
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/fastapi-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
