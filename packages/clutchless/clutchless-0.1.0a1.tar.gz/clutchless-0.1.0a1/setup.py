# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutchless',
 'clutchless.command',
 'clutchless.command.prune',
 'clutchless.domain',
 'clutchless.entrypoints',
 'clutchless.external',
 'clutchless.service',
 'clutchless.spec',
 'clutchless.spec.prune']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'docopt>=0.6.2,<0.7.0',
 'texttable>=1.6.3,<2.0.0',
 'torrentool>=1.1.0,<2.0.0',
 'transmission-clutch>=5.0.0,<6.0.0']

entry_points = \
{'console_scripts': ['clutchless = clutchless.entrypoints.cli:main']}

setup_kwargs = {
    'name': 'clutchless',
    'version': '0.1.0a1',
    'description': 'A CLI tool to manage torrents and their data in Transmission',
    'long_description': "**This is still under active development - use at your own risk!**\n\nClutchless\n----------\n\n.. image:: https://img.shields.io/pypi/v/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI badge\n\n.. image:: https://img.shields.io/pypi/pyversions/clutchless.svg\n    :target: https://pypi.org/project/clutchless\n    :alt: PyPI versions badge\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Black formatter badge\n\n.. image:: https://img.shields.io/pypi/l/clutchless.svg\n    :target: https://en.wikipedia.org/wiki/MIT_License\n    :alt: License badge\n\n.. image:: https://img.shields.io/pypi/dm/clutchless.svg\n    :target: https://pypistats.org/packages/clutchless\n    :alt: PyPI downloads badge\n\n.. image:: https://coveralls.io/repos/github/mhadam/clutchless/badge.svg?branch=develop\n    :target: https://coveralls.io/github/mhadam/clutchless?branch=develop\n\n\nQuick start\n===========\n\nInstall the package:\n\n.. code-block:: console\n\n    $ pip install clutchless\n\nThe ``-h`` flag can be used to bring up documentation, e.g. ``clutchless -h``::\n\n    A tool for working with torrents and their data in the Transmission BitTorrent client.\n\n    Usage:\n        clutchless [options] <command> [<args> ...]\n\n    Options:\n        -a <address>, --address <address>   Address for Transmission (default is http://localhost:9091/transmission/rpc).\n        -h, --help  Show this screen.\n        --version   Show version.\n\n    The available clutchless commands are:\n        add         Add torrents to Transmission (with or without data).\n        find        Locate data that belongs to torrent files.\n        link        For torrents with missing data in Transmission, find the data and fix the location.\n        archive     Copy .torrent files from Transmission for backup.\n        organize    Migrate torrents to a new location, sorting them into separate folders for each tracker.\n        prune       Remove torrents from Transmission with completely missing data.\n\n    See 'clutchless help <command>' for more information on a specific command.\n\nExamples\n********\n\nTo copy all the ``.torrent`` files in Transmission to ``~/torrent_archive``::\n\n    clutchless archive ~/torrent_archive\n\n\nTo add some torrents to Transmission, searching ``~/torrent_archive`` for ``.torrent`` files and finding data in\n``~/torrent_data``::\n\n    clutchless add ~/torrent_archive -d ~/torrent_data\n\nTo look for matching data given a search folder (``~/torrent_data``) and a directory (``~/torrent_files``)\nthat contains ``.torrent`` files::\n\n    clutchless find ~/torrent_files -d ~/torrent_data\n\n\nTo organize torrents into folders under ``~/new_place`` and named by tracker, with ``default_folder`` for ones missing\na folder name for one reason or another::\n\n    clutchless organize ~/new_place -d default_folder\n\nRemove torrents that are completely missing data::\n\n    clutchless prune client\n\nRemove ``.torrent`` files from some folders (``folder1``, ``folder2``) that are found in Transmission::\n\n    clutchless prune folder ~/folder1 ~/folder2\n\nTo associate torrent to their matching data found in any number of folders (in this case just two)::\n\n    clutchless link ~/data_folder_1 ~/data_folder_2\n",
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mhadam/clutchless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
