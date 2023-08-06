# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maquette_cli',
 'maquette_lib',
 'maquette_sdk',
 'maquette_sdk.common',
 'maquette_sdk.sample']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pandavro>=1.5.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'seaborn>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'maquette',
    'version': '0.0.5',
    'description': 'A command line interface for Maquette Data Science and Machine Learning Platform.',
    'long_description': '# Maquette Py\n\nThis project contains the Python implementation of Maquette which includes the CLI and a SDK\n\n\n## Developing maquette-py\n\n`maquette-py` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://www.pyinstaller.org/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation).\n\n```\n$ git clone $REPOSITORY_URL\n$ cd maquette-py\n$ conda create -p ./environment python=3.8\n\n$ poetry install\n```\n\n## Maquette CLI\n\n## Maquette SDK',
    'author': 'Michael Wellner',
    'author_email': 'michaelwellner@kpmg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
