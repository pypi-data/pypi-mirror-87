# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptocmd']

package_data = \
{'': ['*']}

install_requires = \
['pyquery', 'requests', 'tablib']

setup_kwargs = {
    'name': 'cryptocmd',
    'version': '0.5.6',
    'description': 'Cryptocurrency historical market price data scrapper.',
    'long_description': '.. -*-restructuredtext-*-\n\ncryptoCMD: cryptoCurrency Market Data\n======================================\n\n.. image:: https://img.shields.io/pypi/v/cryptoCMD.svg\n    :target: https://pypi.python.org/pypi/cryptoCMD\n\n.. image:: https://travis-ci.org/guptarohit/cryptoCMD.svg?branch=master\n    :target: https://travis-ci.org/guptarohit/cryptoCMD\n    \n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD.svg?type=shield\n    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD?ref=badge_shield\n    :alt: FOSSA Status\n\n.. image:: https://img.shields.io/pypi/l/cryptoCMD.svg\n    :target: https://github.com/guptarohit/cryptoCMD/blob/master/LICENSE\n\n.. image:: https://img.shields.io/pypi/pyversions/cryptoCMD.svg\n    :target: https://pypi.python.org/pypi/cryptoCMD\n\n.. image:: https://pepy.tech/badge/cryptoCMD\n    :target: https://pepy.tech/project/cryptoCMD\n    :alt: Downloads\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Code style: black\n\nCryptocurrency historical market price data scraper written in Python.\n\n\nInstallation\n------------\n\n::\n\n    $ pip install cryptocmd\n\nto install from the latest source use following command\n\n::\n\n    $ pip install git+git://github.com/guptarohit/cryptoCMD.git\n\n\nUsage\n------\n=====================\nCoinMarketCap Scraper\n=====================\n\nFollowing methods are available to get data in multiple formats from https://coinmarketcap.com\n\nTo get all time historical data of a cryptocurrency\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. code:: python\n\n    from cryptocmd import CmcScraper\n\n    # initialise scraper without time interval\n    scraper = CmcScraper("XRP")\n\n    # get raw data as list of list\n    headers, data = scraper.get_data()\n\n    # get data in a json format\n    xrp_json_data = scraper.get_data("json")\n\n    # export the data as csv file, you can also pass optional `name` parameter\n    scraper.export("csv", name="xrp_all_time")\n\n    # Pandas dataFrame for the same data\n    df = scraper.get_dataframe()\n\nTo get data of a cryptocurrency for some days\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. code:: python\n\n    from cryptocmd import CmcScraper\n\n    # initialise scraper with time interval\n    scraper = CmcScraper("XRP", "15-10-2017", "25-10-2017")\n\n    # get raw data as list of list\n    headers, data = scraper.get_data()\n\n    # get data in a json format\n    json_data = scraper.get_data("json")\n\n    # export the data to csv\n    scraper.export("csv")\n\n    # get dataframe for the data\n    df = scraper.get_dataframe()\n\n\nFollowing are the columns of the data\n"""""""""""""""""""""""""""""""""""""\n``Date, Open, High, Low, Close, Volume, Market Cap``\n\n\nAcknowledgements\n----------------\nThe data is being scrapped from `coinmarketcap <https://coinmarketcap.com>`_ :v: and it\'s `free <https://coinmarketcap.com/faq/>`_ to use. :tada:\n\n\nContributing\n------------\n\nFeel free to make a pull request! :octocat:\n\nIf you found this useful, I\'d appreciate your consideration in the below. ✨☕\n\n.. image:: https://user-images.githubusercontent.com/7895001/52529389-e2da5280-2d16-11e9-924c-4fe3f309c780.png\n    :target: https://www.buymeacoffee.com/rohitgupta\n    :alt: Buy Me A Coffee\n\n.. image:: https://user-images.githubusercontent.com/7895001/52529390-e8379d00-2d16-11e9-913b-4d09db90403f.png\n    :target: https://www.patreon.com/bePatron?u=14009502\n    :alt: Become a Patron!\n\n\nLicense\n-------\n\n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD.svg?type=large\n    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD?ref=badge_large\n    :alt: FOSSA Status\n',
    'author': 'Rohit Gupta',
    'author_email': 'rohitgtech+git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guptarohit/cryptoCMD',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
