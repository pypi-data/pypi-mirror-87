# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipapp',
 'ipapp.asgi',
 'ipapp.db',
 'ipapp.http',
 'ipapp.logger',
 'ipapp.logger.adapters',
 'ipapp.mq',
 'ipapp.openapi',
 'ipapp.pytest',
 'ipapp.pytest.qase',
 'ipapp.rpc',
 'ipapp.rpc.http',
 'ipapp.rpc.jsonrpc',
 'ipapp.rpc.jsonrpc.http',
 'ipapp.rpc.jsonrpc.mq',
 'ipapp.rpc.jsonrpc.openrpc',
 'ipapp.rpc.mq',
 'ipapp.s3',
 'ipapp.sftp',
 'ipapp.sphinx',
 'ipapp.task',
 'ipapp.utils',
 'ipapp.utils.lock']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'aiojobs>=0.2.2,<0.4.0',
 'aiozipkin>=0.7,<1.1',
 'async-timeout>=3.0.1,<4.0.0',
 'deepmerge>=0.1.0,<0.2.0',
 'docstring-parser>=0.7.1,<0.8.0',
 'jsonschema>=3.2.0,<4.0.0',
 'prometheus-client>=0.8,<0.10',
 'pydantic>=1.6.1,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'sentry-sdk>=0.18.0,<1.0',
 'tinyrpc>=1.0.4,<2.0.0']

extras_require = \
{'dbtm': ['asyncpg>=0.21.0,<0.22.0', 'crontab>=0.22.6,<0.23.0'],
 'fastapi': ['uvicorn>=0.12.1,<0.13.0', 'fastapi>=0.61,<0.63'],
 'iprpc': ['iprpc>=0.2.3,<0.3.0'],
 'oracle': ['cx-Oracle>=8.0.0,<9.0.0'],
 'postgres': ['asyncpg>=0.21.0,<0.22.0'],
 'rabbitmq': ['pika>=1.1.0,<2.0.0'],
 'redis': ['aioredis>=1.3.1,<2.0.0'],
 's3': ['aiobotocore>=1.0.7,<2.0.0', 'python-magic>=0.4.18,<0.5.0'],
 'sftp': ['asyncssh[pyOpenSSL]>=2.3.0,<3.0.0'],
 'testing': ['black==20.8b1',
             'flake8==3.8.4',
             'mock>=4.0.2,<5.0.0',
             'mypy==0.790',
             'bandit==1.6.2',
             'isort==5.6.4',
             'safety>=1.9.0,<2.0.0',
             'pylint>=2.6.0,<3.0.0',
             'pytest-aiohttp>=0.3.0,<0.4.0',
             'pytest>=6.1.0,<7.0.0',
             'pytest-asyncio>=0.14.0,<0.15.0',
             'pytest-cov>=2.10.0,<3.0.0',
             'coverage[toml]>=5.3,<6.0',
             'Sphinx>=3.2.1,<4.0.0',
             'sphinx-rtd-theme>=0.5.0,<0.6.0',
             'tox>=3.20.0,<4.0.0',
             'async-generator>=1.10,<2.0',
             'docker-compose>=1.27.4,<2.0.0',
             'watchdog>=0.10.3,<0.11.0']}

entry_points = \
{'pytest11': ['pytest_qase = ipapp.pytest.qase.plugin']}

setup_kwargs = {
    'name': 'ipapp',
    'version': '0.6.4',
    'description': 'InPlat application framework',
    'long_description': 'InPlat application framework\n============================\n\n[Докумментация](https://ipapp.readthedocs.io/ru/latest/)\n\n\n\n',
    'author': 'InPlat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inplat/ipapp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
