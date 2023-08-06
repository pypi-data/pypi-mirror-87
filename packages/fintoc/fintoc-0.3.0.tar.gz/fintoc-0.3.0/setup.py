# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fintoc']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.12.1,<0.13.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'fintoc',
    'version': '0.3.0',
    'description': 'The official Python client for the Fintoc API.',
    'long_description': '\n# Fintoc meets :snake:\n![PyPI - Version](https://img.shields.io/pypi/v/fintoc)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fintoc)\n\nYou have just found the [Python](https://www.python.org/)-flavored client of [Fintoc](https://fintoc.com/).\n\n## Why?\n\nYou can think of [Fintoc API](https://fintoc.com/docs) as a piscola.\nAnd the key ingredient to a properly made piscola are the ice cubes.  \nSure, you can still have a [piscola without ice cubes](https://curl.haxx.se/).\nBut hey… that’s not enjoyable -- why would you do that?  \nDo yourself a favor: go grab some ice cubes by installing this refreshing library.\n\n---\n\n## Table of contents\n\n* [How to install](#how-to-install)\n* [Quickstart](#quickstart)\n* [Documentation](#documentation)\n* [Examples](#examples)\n  + [Get accounts](#get-accounts)\n  + [Get movements](#get-movements)\n* [Dependencies](#dependencies)\n* [How to test...](#how-to-test)\n* [Roadmap](#roadmap)\n* [Acknowledgements](#acknowledgements)\n\n## How to install\n\nInstall it with [Poetry](https://python-poetry.org/), the modern package manager.\n\n```sh\n$ poetry add fintoc\n```\n\nDon’t worry: if poetry is not your thing, you can also use [pip](https://pip.pypa.io/en/stable/).\n\n```sh\n$ pip install fintoc\n```\n\n**Note:** This client requires [**Python 3.6+**](https://docs.python.org/3/whatsnew/3.6.html).\n\n## Quickstart\n\n1. Get your API key and link your bank account using the [Fintoc dashboard](https://app.fintoc.com/login).\n2. Open your command-line interface.\n3. Write a few lines of Python to see your bank movements.\n\n```python\n>>> from fintoc import Client\n>>> client = Client("your_api_key")\n>>> link = client.get_link("your_link_token")\n>>> account = link.find(type_="checking_account")\n>>> account.get_movements(since=\'2020-01-01\')\n```\n\nAnd that’s it!\n\n## Documentation\n\nThis client supports all Fintoc API endpoints. For complete information about the API, head to the [docs](https://fintoc.com/docs).\n\n## Examples\n\n### Get accounts\n\n```python\nfrom fintoc import Client\n\nclient = Client("your_api_key")\nlink = client.get_link("your_link_token")\n\nfor account in link:\n    print(account.name)\n\n# Or... you can pretty print all the accounts in a Link\nlink.show_accounts()\n```\n\nIf you want to find a specific account in a link, you can use **find**. You can search by any account field:\n\n```python\naccount = link.find(type_="checking_account")\naccount = link.find(number="1111111")\naccount = link.find(id_="sdfsdf234")\n```\n\nYou can also search for multiple accounts matching a specific criteria with **find_all**:\n\n```python\nclp_accounts = link.find_all(currency="CLP")\n```\n\nTo update the account balance you can use **update_balance**:\n\n```python\naccount.update_balance()\nprint(account.balance.available)\n```\n\n### Get movements\n\n```python\nfrom datetime import date, timedelta\nfrom fintoc import Client\n\nclient = Client("your_api_key")\nlink = client.get_link("your_link_token")\naccount = link.find(type_="checking_account")\n\n# You can get the account movements since a specific datetime\nyesterday = date.today() - timedelta(days=1)\nmovements = account.get_movements(since=yesterday)\n\n# Or... you can use an ISO 8601 formatted string representation of the datetime\nmovements = account.get_movements(since=\'2020-01-01\')\n```\n\nCalling **get_movements** without arguments gets the last 30 movements of the account.\n\n## Dependencies\n\nThis project relies on these useful libraries.\n\n- [**httpx**](https://github.com/encode/httpx) -- a next-generation HTTP client\n- [**tabulate**](https://github.com/astanin/python-tabulate) -- pretty-print tabular data\n- [**python-dateutil**](https://github.com/dateutil/dateutil) -- useful extensions to the standard Python datetime features\n\n## How to test…\n\n### The web API\n\nThat’s a [🍰](https://en.wiktionary.org/wiki/piece_of_cake).\n\n1. Log in into your bank account and send me some money.\n2. Use this library to check if the movement is correct.\n3. You’re welcome.\n\n### The library\n\nYou can run all the [discoverable tests](https://docs.python.org/3/library/unittest.html#test-discovery).\n\n`$ python -m unittest`\n\n## Roadmap\n\n- Add more docstrings\n- Add more unit tests\n- Add more type hints\n\n## Acknowledgements\n\nThis library was initially designed and handcrafted by [**@nebil**](https://github.com/nebil),\n[ad](https://en.wikipedia.org/wiki/Ad_honorem) [piscolem](https://en.wiktionary.org/wiki/piscola).  \nHe built it with the help of Gianni Roberto’s [Picchi 2](https://www.youtube.com/watch?v=WqjUlmkYr2g).\n',
    'author': 'Nebil Kawas',
    'author_email': 'nebil@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fintoc.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
