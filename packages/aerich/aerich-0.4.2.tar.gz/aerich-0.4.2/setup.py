# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerich',
 'aerich.ddl',
 'aerich.ddl.mysql',
 'aerich.ddl.postgres',
 'aerich.ddl.sqlite']

package_data = \
{'': ['*']}

install_requires = \
['click', 'pydantic', 'tortoise-orm']

extras_require = \
{'dbdrivers': ['aiomysql', 'asyncpg']}

entry_points = \
{'console_scripts': ['aerich = aerich.cli:main']}

setup_kwargs = {
    'name': 'aerich',
    'version': '0.4.2',
    'description': 'A database migrations tool for Tortoise ORM.',
    'long_description': '# Aerich\n\n[![image](https://img.shields.io/pypi/v/aerich.svg?style=flat)](https://pypi.python.org/pypi/aerich)\n[![image](https://img.shields.io/github/license/long2ice/aerich)](https://github.com/long2ice/aerich)\n[![image](https://github.com/long2ice/aerich/workflows/pypi/badge.svg)](https://github.com/long2ice/aerich/actions?query=workflow:pypi)\n[![image](https://github.com/long2ice/aerich/workflows/test/badge.svg)](https://github.com/long2ice/aerich/actions?query=workflow:test)\n\n## Introduction\n\nAerich is a database migrations tool for Tortoise-ORM, which like alembic for SQLAlchemy, or Django ORM with it\\\'s\nown migrations solution.\n\n**Important: You can only use absolutely import in your `models.py` to make `aerich` work.**\n\n## Install\n\nJust install from pypi:\n\n```shell\n> pip install aerich\n```\n\n## Quick Start\n\n```shell\n> aerich -h\n\nUsage: aerich [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -c, --config TEXT  Config file.  [default: aerich.ini]\n  --app TEXT         Tortoise-ORM app name.  [default: models]\n  -n, --name TEXT    Name of section in .ini file to use for aerich config.\n                     [default: aerich]\n  -h, --help         Show this message and exit.\n\nCommands:\n  downgrade  Downgrade to specified version.\n  heads      Show current available heads in migrate location.\n  history    List all migrate items.\n  init       Init config file and generate root migrate location.\n  init-db    Generate schema and generate app migrate location.\n  migrate    Generate migrate changes file.\n  upgrade    Upgrade to latest version.\n```\n\n## Usage\n\nYou need add `aerich.models` to your `Tortoise-ORM` config first,\nexample:\n\n```python\nTORTOISE_ORM = {\n    "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"},\n    "apps": {\n        "models": {\n            "models": ["tests.models", "aerich.models"],\n            "default_connection": "default",\n        },\n    },\n}\n```\n\n### Initialization\n\n```shell\n> aerich init -h\n\nUsage: aerich init [OPTIONS]\n\n  Init config file and generate root migrate location.\n\nOptions:\n  -t, --tortoise-orm TEXT  Tortoise-ORM config module dict variable, like settings.TORTOISE_ORM.\n                           [required]\n  --location TEXT          Migrate store location.  [default: ./migrations]\n  -h, --help               Show this message and exit.\n```\n\nInit config file and location:\n\n```shell\n> aerich init -t tests.backends.mysql.TORTOISE_ORM\n\nSuccess create migrate location ./migrations\nSuccess generate config file aerich.ini\n```\n\n### Init db\n\n```shell\n> aerich init-db\n\nSuccess create app migrate location ./migrations/models\nSuccess generate schema for app "models"\n```\n\nIf your Tortoise-ORM app is not default `models`, you must specify\n`--app` like `aerich --app other_models init-db`.\n\n### Update models and make migrate\n\n```shell\n> aerich migrate --name drop_column\n\nSuccess migrate 1_202029051520102929_drop_column.sql\n```\n\nFormat of migrate filename is\n`{version_num}_{datetime}_{name|update}.sql`.\n\nAnd if `aerich` guess you are renaming a column, it will ask `Rename {old_column} to {new_column} [True]`, you can choice `True` to rename column without column drop, or choice `False` to drop column then create.\n\n### Upgrade to latest version\n\n```shell\n> aerich upgrade\n\nSuccess upgrade 1_202029051520102929_drop_column.sql\n```\n\nNow your db is migrated to latest.\n\n### Downgrade to specified version\n\n```shell\n> aerich init -h\n\nUsage: aerich downgrade [OPTIONS]\n\n  Downgrade to specified version.\n\nOptions:\n  -v, --version INTEGER  Specified version, default to last.  [default: -1]\n  -d, --delete           Delete version files at the same time.  [default:\n                         False]\n\n  --yes                  Confirm the action without prompting.\n  -h, --help             Show this message and exit.\n```\n\n```shell\n> aerich downgrade\n\nSuccess downgrade 1_202029051520102929_drop_column.sql\n```\n\nNow your db rollback to specified version.\n\n### Show history\n\n```shell\n> aerich history\n\n1_202029051520102929_drop_column.sql\n```\n\n### Show heads to be migrated\n\n```shell\n> aerich heads\n\n1_202029051520102929_drop_column.sql\n```\n\n### Multiple databases\n\n```python\ntortoise_orm = {\n    "connections": {\n        "default": expand_db_url(db_url, True),\n        "second": expand_db_url(db_url_second, True),\n    },\n    "apps": {\n        "models": {"models": ["tests.models", "aerich.models"], "default_connection": "default"},\n        "models_second": {"models": ["tests.models_second"], "default_connection": "second",},\n    },\n}\n```\n\nYou need only specify `aerich.models` in one app, and must specify `--app` when run `aerich migrate` and so on.\n\n## Support this project\n\n| AliPay                                                                                 | WeChatPay                                                                                 | PayPal                                                           |\n| -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |\n| <img width="200" src="https://github.com/long2ice/aerich/raw/dev/images/alipay.jpeg"/> | <img width="200" src="https://github.com/long2ice/aerich/raw/dev/images/wechatpay.jpeg"/> | [PayPal](https://www.paypal.me/long2ice) to my account long2ice. |\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/aerich/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/aerich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
