# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsu', 'fsu.internal']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0',
 'fastapi>=0.57.0,<1.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'orjson>=3.0.1,<4.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'sqlalchemy>=1.3.17,<2.0.0']

setup_kwargs = {
    'name': 'fsu',
    'version': '2.4.3',
    'description': 'FastAPI, SQLAlchemy core Utils and more',
    'long_description': None,
    'author': 'Lutz',
    'author_email': 'lutz.l.burning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
