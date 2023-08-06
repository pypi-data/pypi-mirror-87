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
    'version': '1.0.0',
    'description': 'A webscraper for Daft.ie',
    'long_description': "# daft-scraper\n\n- [daft-scraper](#daft-scraper)\n- [Install](#install)\n  - [Via Pip](#via-pip)\n  - [Via Git](#via-git)\n- [Example Usage](#example-usage)\n- [Using the CLI](#using-the-cli)\n  - [`search` command](#search-command)\n\n\n# Install\n\n## Via Pip\nYou can install the library using pip:\n\n```\npip install daft-scraper\n```\n\n## Via Git\nThe project uses [poetry](https://python-poetry.org/), so you'll need poetry to install the dependencies and setup the project.\n\n```\ngit clone git@github.com:TheJokersThief/daft-scraper.git\ncd daft-scraper\nmake install\n```\n\n# Example Usage\n\n```python\nfrom daft_scraper.search import DaftSearch, SearchType\nfrom daft_scraper.search.options import (\n    PropertyType, PropertyTypesOption, Facility, FacilitiesOption,\n    PriceOption, BedOption\n)\nfrom daft_scraper.search.options_location import LocationsOption, Location\n\napi = DaftSearch(SearchType.RENT)\nlistings = api.search(options)\n\nprint(len(listings))\nfor listing in listings:\n    print(listing.get('title'))\n\n```\n\n# Using the CLI\n\nTo install the CLI, clone the repo and install the dependencies with `make install`.\n\n```\n$ poetry run daft search --max-pages 1 property-for-rent\n     id    price  title                                                                       propertyType\n-------  -------  --------------------------------------------------------------------------  --------------\n1443907     2800  Capital Dock Residence, Grand Canal, Grand Canal Dock, Co. Dublin           Apartments\n1446982     2500  Quayside Quarter, North Wall Quay, Dublin 1, Co. Dublin                     Apartments\n1442724     2850  Opus, 6 Hanover Quay, Hanover Quay, Dublin 2, Co. Dublin                    Apartments\n2621605     1900  Knockrabo, Mount Anville Road, Goatstown, Co. Dublin                        Apartments\n2503954     2500  OCCU Scholarstown Wood, Scholarstown Road, Rathfarnham, Co. Dublin          Apartments\n2511232     1900  Clancy Quay by Kennedy Wilson, South Circular Road, Dublin 8, Co. Dublin    Apartments\n2314852     1700  Elmfield by Havitat, Ballyogan Road, Leopardstown, Co. Dublin               Apartments\n1442430     2150  Mount Argus Apartments, Mount Argus Road, Harold's Cross, Co. Dublin        Apartments\n1491037     1950  Bridgefield, Northwood, Santry, Co. Dublin                                  Apartments\n2621761      430  Archway Court Student Accommodation, Mountjoy Street, Dublin 7, Co. Dublin  Apartments\n2524873     2200  Ropemaker Place, Hanover Street East, Dublin 2, Co. Dublin                  Apartments\n2329824     1750  Wolfe Tone Lofts by Havitat, Wolfe Tone Street, Dublin 1, Co. Dublin        Apartments\n2632723     2000  Heuston South Quarter, St Johns Road West, Dublin 8, Co. Dublin             Apartments\n1527608     2808  Node Living, 25 pembroke street upper, Dublin 2, Co. Dublin                 Apartments\n2317385     1900  Sandford Lodge by Kennedy Wilson, Sandford Lodge, Ranelagh, Co. Dublin      Apartments\n2524752     2350  Whitepines South, Stocking Avenue, Rathfarnham, Co. Dublin                  Apartments\n1518281     1850  Marina Village, Greystones, Co. Wicklow                                     Apartments\n2287912     1750  Hanbury Mews, Hanbury Lane, Dublin 8, Co. Dublin                            Apartments\n2316503     2600  Alto Vetro, Grand Canal Square, Dublin 2, Co. Dublin                        Apartments\n2317419     1800  Northbank Apartments, Castleforbes Road, Dublin 1, Co. Dublin               Apartments\n```\n\n## `search` command\n\n| argument  | description |\n|---|---|\n| search_type | The type of search you want to initiate. For the possible values, check out the [SearchType Enum](daft_scraper/search/__init__.py). |\n\nFor any flag that can take `[multiple]` arguments, you can supply the flag multiple times.\n\n| flag  | description |\n|---|---|\n| --headers | The attributes to print out for each listing. [multiple] |\n| --locations | Which location you want to search for. For all the possible values, check out the [Location Enum](daft_scraper/search/options_location.py) [multiple] |\n| --max-pages | Each page is 20 results, this sets the limit on the number of pages fetched. |\n| --min-price | Minimum price. |\n| --max-price | Maximum price. |\n| --min-beds | Minimum number of bedrooms. |\n| --max-beds | Maximum number of bedrooms. |\n| --min-lease | Minimum term on the lease (in months). |\n| --max-lease | Maximum term on the lease (in months). |\n| --property-type | The type of property to search for. For all possible values, checkout the [PropertyType Enum](/daft_scraper/search/options.py) |\n| --facility | Which facilities must the listing include. [multiple] |\n| --media-type | Which media types must the listing include. [multiple] |\n| --sort | How should the results be sorted. For all possible views, check out the [Sort Enum](daft_scraper/search/options). |\n| --furnishing | Should the listing be furnished or unfurnished. |\n",
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
