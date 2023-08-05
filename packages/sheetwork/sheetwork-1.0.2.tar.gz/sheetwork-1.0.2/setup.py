# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheetwork',
 'sheetwork.core',
 'sheetwork.core.adapters',
 'sheetwork.core.adapters.base',
 'sheetwork.core.clients',
 'sheetwork.core.config',
 'sheetwork.core.task',
 'sheetwork.core.ui',
 'sheetwork.core.yaml']

package_data = \
{'': ['*']}

install_requires = \
['cerberus>=1.3.2,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'gspread>=3,<4',
 'inflection>=0.5.1,<0.6.0',
 'luddite>=1.0.1,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'packaging>=20.4,<21.0',
 'pandas>=1.1.2,<1.2.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests<2.23.0',
 'retrying>=1.3.3,<2.0.0',
 'snowflake-sqlalchemy>=1,<2',
 'sqlalchemy>=1.3.19,<2.0.0']

entry_points = \
{'console_scripts': ['sheetwork = sheetwork.core.main:main']}

setup_kwargs = {
    'name': 'sheetwork',
    'version': '1.0.2',
    'description': 'A handy CLI tool to ingest GoogleSheets into your database without writing a single line of code',
    'long_description': '![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/bastienboutonnet/sheetwork?include_prereleases) [![codecov](https://codecov.io/gh/bastienboutonnet/sheetwork/branch/dev%2Fnicolas_jaar/graph/badge.svg)](https://codecov.io/gh/bastienboutonnet/sheetwork)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/bastienboutonnet/sheetwork/dev/nicolas_jaar.svg)](https://results.pre-commit.ci/latest/github/bastienboutonnet/sheetwork/dev/nicolas_jaar)\n![Sheetwork Build](https://github.com/bastienboutonnet/sheetwork/workflows/Sheetwork%20CI/badge.svg)\n![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)\n[![Discord](https://img.shields.io/discord/752101657218908281?label=discord)](https://discord.gg/ebSTWq)\n\n# sheetwork 💩🤦\n\n## What is sheetwork?\n\nsheetwork is a handy open-source CLI-tool that allows non-coders to ingest Google Spreadsheets directly into their databases with control over data types, renaming, basic data sanitisation etc.\n\nIt offers a "close to no code" workflow that can still live alongside your codebase as all configuration lives in text files and is easily version-controllable. This makes it an ideal tool for teams.\n\n> ⚠️ **warning** `sheetwork` is still in its early inception (don\'t get fooled by the 1 in the version). Please do some testing before you end up using it in production, and feel free to report bugs.\n\n> **compatibility**:\n>\n> - Python: 3.6, 3.7, 3.8\n>   OS: Mac OSX >10.14, Linux\n> - So far all our unit tests work on Windows (tested in GitHub Actions) but no comprehensive testing has been done on this platform.\n> - sheetwork currently only offers support for cloud database Snowflake. However, its design follows an adapter pattern (currently in the making) and can be extended to interact with most databases. Feel free to check how you can [contribute](CONTRIBUTING.md) to the project or reach out on [Discord](https://discord.gg/5GnNNb)..\n\n## Why use sheetwork?\n\nGetting google sheets into any database often requires writing custom Python code that interacts with the Google API. That\'s fine if you can write Python, but it may not always be an option. On top of that, if your workflow requires you to ingest a bunch of sheets you may find yourself **writing the same boiler plate code over and over**. Sheetwork offers a way to bring some DRY practices, standardisation, and simplification to basic google sheet ingestion. **It won\'t do a lot of transformations and doesn\'t have room for baking in much transformational logic because we believe this is best done by fully-fledged ETL open-source tools such as [dbt](https://www.getdbt.com/)**.\n\nA handy package to load Google Sheets to your database right from the CLI and with easy configuration via YAML files.\n\n🙋🏻\u200d♂️ **Want to use `sheetwork` on other databases? Let\'s talk!** ([Make an issue](https://github.com/bastienboutonnet/sheetwork/issues/new/choose), or ping me on [Discord](https://discord.gg/5GnNNb))\n\n## Installation & Documentation\n\nHead over to the pretty [documentation](https://bastienboutonnet.gitbook.io/sheetwork/).\n',
    'author': 'Bastien Boutonnet',
    'author_email': 'bastien.b1@gmail.com',
    'maintainer': 'Bastien Boutonnet',
    'maintainer_email': 'bastien.b1@gmail.com',
    'url': 'https://github.com/bastienboutonnet/sheetwork',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
