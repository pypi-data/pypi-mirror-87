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
 'tabulate>=0.8.7,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['daft = daft_scraper.cli:main']}

setup_kwargs = {
    'name': 'daft-scraper',
    'version': '1.0.2',
    'description': 'A webscraper for Daft.ie',
    'long_description': "# daft-scraper\n\n[![TheJokersThief](https://circleci.com/gh/TheJokersThief/daft-scraper.svg?style=svg)](<LINK>)\n\n- [daft-scraper](#daft-scraper)\n- [Install](#install)\n  - [Via Pip](#via-pip)\n  - [Via Git](#via-git)\n- [Example Usage](#example-usage)\n- [Using the CLI](#using-the-cli)\n  - [`search` command](#search-command)\n\n\n# Install\n\n## Via Pip\nYou can install the library using pip:\n\n```\npip install daft-scraper\n```\n\n## Via Git\nThe project uses [poetry](https://python-poetry.org/), so you'll need poetry to install the dependencies and setup the project.\n\n```\ngit clone git@github.com:TheJokersThief/daft-scraper.git\ncd daft-scraper\nmake install\n```\n\n# Example Usage\n\n```python\nfrom daft_scraper.search import DaftSearch, SearchType\nfrom daft_scraper.search.options import (\n    PropertyType, PropertyTypesOption, Facility, FacilitiesOption,\n    PriceOption, BedOption\n)\nfrom daft_scraper.search.options_location import LocationsOption, Location\n\napi = DaftSearch(SearchType.RENT)\nlistings = api.search(options)\n\nprint(len(listings))\nfor listing in listings:\n    print(listing.get('title'))\n\n```\n\n# Using the CLI\n\nTo install the CLI, clone the repo and install the dependencies with `make install`.\n\n```\n$ poetry run daft search --max-pages 1 property-for-rent --location cork --location galway\n     id    price  title                                                                    propertyType\n-------  -------  -----------------------------------------------------------------------  --------------\n2315059     3328  The Elysian, Eglinton Road, Co. Cork                                     Apartments\n2588837      570  Parchment Square, Model Farm Road, Cork, Co. Cork                        Apartments\n2310295      175  Nido Curraheen Point, Farranlea Road, Co. Cork                           Apartments\n2292251      220  From Here - Student Living, Galway Central, Fairgreen Road, Co. Galway   Apartments\n2590894      495  BUNK CO LIVING, Kiltartan house Forster Street, Co. Galway               Apartments\n2575994      650  Steelworks, 9/10 Copley Street, Ballintemple, Cork City, Cork, Co. Cork  Apartments\n2327420      237  Lee Point, South Main Street, Co. Cork                                   Apartments\n2751036     2400  16A The Long Walk, Co. Galway                                            House\n2745585     1588  Wellington Road, Co. Cork                                                Apartment\n2626561     2800  3 Saint Joseph's Terrace, Gould Street, Co. Cork                         House\n2737101     1800  CHURCHFIELDS SALTHILL, Salthill, Co. Galway                              House\n2759058     1400  24 Rutland Place, South Terrace, Co. Cork                                Apartment\n2629695     1750  56 Caiseal Cam, Roscam, Co. Galway                                       House\n2737848     1500  Dark Rd, Kilcolgan, Co. Galway                                           House\n2737834     1800  11 Shangort Park, Knocknacarra, Co. Galway                               House\n2757337      950  Apartment 3, 13 Harbour Row, Cobh, Co. Cork                              House\n2756288     4500  Meizelljob, Coast Road, Fountainstown, Co. Cork                          House\n2756231     1500  Garrai De Brun, Fort Lorenzo, Taylor's Hill, Co. Galway                  House\n2632714     1650  3 Bothar An tSlÃ©ibhe, Moycullen, Co. Galway                             House\n2750256     1900  Grealishtown, Bohermore, Co. Galway                                      House\n```\n\n## `search` command\n\n| argument  | description |\n|---|---|\n| search_type | The type of search you want to initiate. For the possible values, check out the [SearchType Enum](daft_scraper/search/__init__.py). |\n\nFor any flag that can take `[multiple]` arguments, you can supply the flag multiple times.\n\n| flag  | description |\n|---|---|\n| --headers | The attributes to print out for each listing. [multiple] |\n| --location | Which location you want to search for. For all the possible values, check out the [Location Enum](daft_scraper/search/options_location.py) [multiple] |\n| --max-pages | Each page is 20 results, this sets the limit on the number of pages fetched. |\n| --min-price | Minimum price. |\n| --max-price | Maximum price. |\n| --min-beds | Minimum number of bedrooms. |\n| --max-beds | Maximum number of bedrooms. |\n| --min-lease | Minimum term on the lease (in months). |\n| --max-lease | Maximum term on the lease (in months). |\n| --property-type | The type of property to search for. For all possible values, checkout the [PropertyType Enum](/daft_scraper/search/options.py) |\n| --facility | Which facilities must the listing include. [multiple] |\n| --media-type | Which media types must the listing include. [multiple] |\n| --sort | How should the results be sorted. For all possible views, check out the [Sort Enum](daft_scraper/search/options). |\n| --furnishing | Should the listing be furnished or unfurnished. |\n",
    'author': 'Evan Smith',
    'author_email': 'me@iamevan.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
