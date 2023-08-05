# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pympg', 'pympg.gen']

package_data = \
{'': ['*']}

install_requires = \
['questionary>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['pympg = pympg.cli:main']}

setup_kwargs = {
    'name': 'pympg',
    'version': '0.0.2',
    'description': 'Command-line multipurpose generator.',
    'long_description': '# ![Config Icon](https://www.iconfinder.com/icons/1976051/download/png/64)pympg\n\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n\n[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)\n\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\nCommand-line multipurpose config generator.\n\n## Example\n\n![Example GIF](./assets/pympg-example.gif)\n\n## Prerequisites\n\n-   Latest version of Python 3\n-   For apache2 config generation, apache2 (and it\'s proxy modules enabled).\n\n## Installation\n\n-   Run `pip3 install pympg` to install this package.\n-   Run `sudo pympg` to open the generation prompt.\n\n## Development Build Instructions\n\n### Prerequisites\n\n-   Python 3\n-   Python poetry\n\n### Building\n\n-   `git clone https://github.com/throw-out-error/pympg.git`\n-   CD into the folder\n-   Run `./build.sh` to build the package and install it.\n-   Run `sudo pympg` to run pympg\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://onyxcode.net"><img src="https://avatars1.githubusercontent.com/u/58049576?v=4" width="100px;" alt=""/><br /><sub><b>Dan</b></sub></a><br /><a href="https://github.com/throw-out-error/pympg/commits?author=onyxcode" title="Code">💻</a></td>\n    <td align="center"><a href="https://theoparis.com/about"><img src="https://avatars0.githubusercontent.com/u/11761863?v=4" width="100px;" alt=""/><br /><sub><b>Theo Paris</b></sub></a><br /><a href="https://github.com/throw-out-error/pympg/commits?author=creepinson" title="Documentation">📖</a> <a href="https://github.com/throw-out-error/pympg/commits?author=creepinson" title="Code">💻</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-enable -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Theo Paris',
    'author_email': 'theoparisdesigns@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
