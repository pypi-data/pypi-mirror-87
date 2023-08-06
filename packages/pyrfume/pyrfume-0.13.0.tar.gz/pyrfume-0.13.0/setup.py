# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrfume', 'pyrfume.unit_test']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0',
 'dask[bag]>=2.17.0,<3.0.0',
 'datajoint>=0.12.6b1',
 'deap>=1.3.1',
 'eden-kernel>=0.3.1335',
 'flake8>=3.8.2',
 'ipython>=7.14.0',
 'ipywidgets>=7.5.1',
 'isort>=4.3.21',
 'matplotlib>=3.2.1',
 'mordred>=1.2.0',
 'numpy>=1.18.4',
 'pandas>=1.0.3',
 'plotly>=4.8.0',
 'pubchempy>=1.0.4',
 'quantities>=0.12.4',
 'scikit-learn>=0.23.1',
 'scipy>=1.4.1',
 'sympy>=1.6',
 'tqdm>=4.46.0']

setup_kwargs = {
    'name': 'pyrfume',
    'version': '0.13.0',
    'description': 'A validation library for human olfactory psychophysics research.',
    'long_description': '# Pyrfume\n\n![Pyrfume logo](https://avatars3.githubusercontent.com/u/34174393?s=200&v=4)\n\n#### `pyrfume` is a python library for olfactory psychophysics research. See "notebooks" for examples of use.\n[![Travis](https://travis-ci.org/pyrfume/pyrfume.svg?branch=master)](https://travis-ci.org/pyrfume/pyrfume) \n[![Coverage Status](https://coveralls.io/repos/github/pyrfume/pyrfume/badge.svg?branch=master)](https://coveralls.io/github/pyrfume/pyrfume?branch=master)\n\n### Examples:\n#### Note: these require the Pyrfume data library, *provided separately*.\n```\n# Get raw data from the Sigma Fragrance & Flavor Catalog\nfrom pyrfume import sigma_ff\ndescriptors, data = sigma_ff.get_data()\n\n# Get a PubChem CID-indexed dataframe of the odorant and descriptor data from that catalog:\nimport pyrfume\nsigma = pyrfume.load_data(\'sigma/sigma.csv\')\n```\n### [Website](http://pyrfume.org)\n\n### [Data Curation Status](http://status.pyrfume.org)\n\n### [Docs](https://pyrfume.readthedocs.io/)\n',
    'author': 'Rick Gerkin',
    'author_email': 'rgerkin@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://pyrfume.scidash.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
