# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deshima_sensitivity']

package_data = \
{'': ['*'], 'deshima_sensitivity': ['data/*']}

install_requires = \
['jupyter-io>=0.2,<0.3',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.17,<2.0',
 'pandas>=0.25,<1.1',
 'scipy>=1.4,<2.0']

setup_kwargs = {
    'name': 'deshima-sensitivity',
    'version': '0.2.6',
    'description': 'Sensitivity calculator for DESHIMA-type spectrometers',
    'long_description': '# deshima-sensitivity\n\n[![PyPI](https://img.shields.io/pypi/v/deshima-sensitivity.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/deshima-sensitivity/)\n[![Python](https://img.shields.io/pypi/pyversions/deshima-sensitivity.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/deshima-sensitivity/)\n[![Test](https://img.shields.io/github/workflow/status/deshima-dev/deshima-sensitivity/Test?logo=github&label=Test&style=flat-square)](https://github.com/deshima-dev/deshima-sensitivity/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3966839-blue?style=flat-square)](https://doi.org/10.5281/zenodo.3966839)\n\nSensitivity calculator for DESHIMA-type spectrometers\n\n## Overview\n\ndeshima-sensitivity is a Python package which enables to calculate observation sensitivity of DESHIMA-type spectrometers.\nCurrently it is mainly used to estimate the observation sensitivity of [DESHIMA](http://deshima.ewi.tudelft.nl) and its successors.\n\nAn online Jupyter notebook is available for DESHIMA collaborators to calculate the sensitivity and the mapping speed of the DESHIMA 2.0 by themselves.\nClick the budge below to open it in [Google colaboratory](http://colab.research.google.com/) (a Google account is necessary to re-run it).\n\n### Stable version (recommended)\n\n[![open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deshima-dev/deshima-sensitivity/blob/v0.2.6/sensitivity.ipynb)\n\n### Latest version\n\n[![open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deshima-dev/deshima-sensitivity/blob/master/sensitivity.ipynb)\n\nIn the case of running it in a local Python environment, please follow the requirements and the installation guide below.\n\n## Requirements\n\n- **Python:** 3.6, 3.7, or 3.8 (tested by the authors)\n- **Dependencies:** See [pyproject.toml](https://github.com/deshima-dev/deshima-sensitivity/blob/master/pyproject.toml)\n\n## Installation\n\n```shell\n$ pip install deshima-sensitivity\n```\n',
    'author': 'Akira Endo',
    'author_email': 'a.endo@tudelft.nl',
    'maintainer': 'Akio Taniguchi',
    'maintainer_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'url': 'https://github.com/deshima-dev/deshima-sensitivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
