# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.devkit']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'coverage>=5.0.3,<6.0.0',
 'flake8-breakpoint>=1.1.0,<2.0.0',
 'flake8-builtins>=1.5.2,<2.0.0',
 'flake8-colors>=0.1.6,<0.2.0',
 'flake8-commas>=2.0.0,<3.0.0',
 'flake8-debugger>=3.2.1,<4.0.0',
 'flake8-if-expr>=1.0.0,<2.0.0',
 'flake8-mutable>=1.2.0,<2.0.0',
 'flake8-print>=3.1.4,<5.0.0',
 'flake8-pytest>=1.3,<2.0',
 'flake8-return>=1.1.1,<2.0.0',
 'flake8>=3.7.9,<4.0.0',
 'ipython>=7.13.0,<8.0.0',
 'isort>=4.3.21,<5.0.0',
 'mock>=4.0.2,<5.0.0',
 'mypy>=0.780,<0.791',
 'outcome-utils>=4.11.0,<5.0.0',
 'pactman>=2.28.0,<3.0.0',
 'pdbpp>=0.10.2,<0.11.0',
 'pre-commit>=2.2.0,<3.0.0',
 'pytest-asyncio>=0.12,<0.15',
 'pytest>=5.3.5,<7.0.0',
 'wemake-python-styleguide>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'outcome-devkit',
    'version': '3.4.7',
    'description': 'A package containing common dev dependencies for python projects.',
    'long_description': '# devkit-py\n![ci-badge](https://github.com/outcome-co/devkit-py/workflows/Release/badge.svg?branch=v3.4.7) ![version-badge](https://img.shields.io/badge/version-3.4.7-brightgreen)\n\nA package containing common dev dependencies for python projects.\n\n## Usage\n\n```sh\npoetry add -D outcome-devkit\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n',
    'author': 'Douglas Willcocks',
    'author_email': 'douglas@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/devkit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<3.9.0',
}


setup(**setup_kwargs)
