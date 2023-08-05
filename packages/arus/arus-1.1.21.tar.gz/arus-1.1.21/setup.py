# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arus',
 'arus.accelerometer',
 'arus.core',
 'arus.core.tests',
 'arus.dataset',
 'arus.extensions',
 'arus.feature_vector',
 'arus.mhealth_format',
 'arus.models',
 'arus.plugins',
 'arus.spades_lab',
 'arus.tests']

package_data = \
{'': ['*'], 'arus.dataset': ['data/*'], 'arus.models': ['prebuilt/*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'joblib>=0.17.0,<0.18.0',
 'loguru>=0.5.0,<0.6.0',
 'loky>=2.6.0,<3.0.0',
 'matplotlib>=3.1,<4.0',
 'numpy==1.19.3',
 'pandas>=1.0.0,<2.0.0',
 'pathos>=0.2.5,<0.3.0',
 'pyarrow>=2.0.0,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.3,<2.0',
 'seaborn>=0.11.0,<0.12.0',
 'tqdm>=4.48.0,<5.0.0',
 'tzlocal>=2.0.0,<3.0.0',
 'wget>=3.2,<4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'demo': ['playsound>=1.2.2,<2.0.0',
          'pymetawear>=0.12.0,<0.13.0',
          'pysimplegui>=4.14.1,<5.0.0'],
 'dev': ['dephell_versioning>=0.1.2,<0.2.0', 'semver>=2.10.1,<3.0.0'],
 'metawear': ['pymetawear>=0.12.0,<0.13.0'],
 'nn': ['tensorboard>=2.3.0,<3.0.0'],
 'nn:sys_platform == "linux"': ['torch>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['arus = arus.cli:cli']}

setup_kwargs = {
    'name': 'arus',
    'version': '1.1.21',
    'description': 'Activity Recognition with Ubiquitous Sensing',
    'long_description': '# Overview\n\n__ARUS__ python package provides a computational and experimental framework to manage and process sensory data or wireless devices, to develop and run activity recognition algorithms on the data, and to create interactive programs using the algorithms and wireless devices.\n\nThis package is licensed under [GPL version 3](https://qutang.github.io/arus/LICENSE/).\n\n[![PyPI version](https://badge.fury.io/py/arus.svg)](https://badge.fury.io/py/arus)  \n[![Downloads](https://pepy.tech/badge/arus)](https://pepy.tech/project/arus)  \n[![deployment build](https://github.com/qutang/arus/workflows/deploy/badge.svg)](https://github.com/qutang/arus/actions?query=workflow%3Adeploy)  \n[![unittest and build test](https://github.com/qutang/arus/workflows/unittest%20and%20build%20test/badge.svg)](https://github.com/qutang/arus/actions?query=workflow%3A%22unittest+and+build+test%22)  \n[![codecov](https://codecov.io/gh/qutang/arus/branch/master/graph/badge.svg)](https://codecov.io/gh/qutang/arus)  \n\n## Prerequists\n\n```bash\npython >= 3.7.0\n```\n\n```bash\n# Need these SDKs to install arus[metawear] on Windows.\nVisual Studio C++ SDK (v14.1)\nWindows SDK (10.0.16299.0)\nWindows SDK (10.0.17763.0)\n\n# Need these packages to install arus[metawear] on Ubuntu or equivalent packages on other linux distributions.\nlibbluetooth-dev\nlibboost-all-dev\nbluez\n```\n\n## Installation\n\n```bash\n> pip install arus\n# Optionally, you may install plugins via pip extra syntax.\n> pip install arus[metawear]\n> pip install arus[demo]\n> pip install arus[dev]\n> pip install arus[nn]\n```\n\n## Optional components\n\n`arus[metawear]`: This optional component installs dependency supports for streaming data from Bluetooth metawear sensors.\n\n`arus[demo]`: This optional component installs dependency supports for running the demo app that demonstrates a real-time interactive activity recognition training and testing program.\n\n`arus[dev]`: These optional component installs dependency supports for running some package and version management functions in the `arus.dev` module.\n\n`arus[nn]`: The optional component installs dependency supports for PyTorch and Tensorboard, which are required by `arus.models.report` module. Note that for Windows, you should install the `torch` package manually using `pip` following the `pytorch.org` instruction.\n\n## Get started for development\n\n```bash\n> git clone https://github.com/qutang/arus.git\n> cd arus\n> # Install poetry python package management tool https://python-poetry.org/docs/\n> # On Linux\n> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n> # On windows powershell\n> (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python\n> # Install package dependencies\n> poetry install\n> # Install optional component dependencies\n> poetry install --extras "metawear demo dev nn"\n> # Run unit tests\n> poetry run pytest\n```\n\n### Development conventions\n\n1. Use Google\'s python coding guidance: http://google.github.io/styleguide/pyguide.html.\n2. Use `arus package release VERSION --release` to bump and tag versions. `VERSION` can be manual version code following semantic versioning, `path`, `minor`, or `major`.\n3. Changelogs are automatically generated when building the documentation website, do not create it manually.\n4. Pypi release will be handled by github action `deploy.yml`, which will be triggered whenever a new tag is pushed. Therefore, developers should only tag release versions.\n5. After commits, even not bumping and releasing the package, you may run `arus package docs --release` to update the documentation website, where the developer version changelogs will be updated immediately.',
    'author': 'qutang',
    'author_email': 'tqshelly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qutang/arus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
