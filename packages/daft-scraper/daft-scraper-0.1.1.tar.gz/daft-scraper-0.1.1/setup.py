# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daft_scraper', 'daft_scraper.cli', 'daft_scraper.search']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'marshmallow>=3.9.1,<4.0.0',
 'requests>=2.25.0,<3.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'daft-scraper',
    'version': '0.1.1',
    'description': 'A webscraper for Daft.ie',
    'long_description': '# daft-scraper',
    'author': 'Evan Smith',
    'author_email': 'me@iamevan.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
