# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_dev_deps']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.2.0,<3.3.0',
 'autopep8>=1.5.4,<2.0.0',
 'black>=20.8b1,<21.0',
 'doc8>=0.8.1,<0.9.0',
 'flake8-type-annotations>=0.1.0,<0.2.0',
 'flake8>=3.8.4,<4.0.0',
 'ipdb>=0.13.4,<0.14.0',
 'm2r2>=0.2.7,<0.3.0',
 'mypy>=0.790,<0.791',
 'pipdeptree>=1.0.0,<2.0.0',
 'pre-commit>=2.9.2,<3.0.0',
 'pylint>=2.6.0,<3.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest-benchmark>=3.2.3,<4.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest-datadir>=1.3.1,<2.0.0',
 'pytest-datafiles>=2.0,<3.0',
 'pytest-freezegun>=0.4.2,<0.5.0',
 'pytest-mock>=3.3.1,<4.0.0',
 'pytest-profiling>=1.7.0,<2.0.0',
 'pytest-randomly>=3.5.0,<4.0.0',
 'pytest-vcr>=1.0.2,<2.0.0',
 'pytest-voluptuous>=1.2.0,<2.0.0',
 'pytest-xdist>=2.1.0,<3.0.0',
 'pytest>=6.1.2,<7.0.0',
 'readme-renderer[md]>=28.0,<29.0',
 'requests-mock>=1.8.0,<2.0.0',
 'setuptools>=50.3.2,<51.0.0',
 'sphinx-autoapi>=1.5.1,<2.0.0',
 'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
 'sphinx-rtd-theme>=0.5.0,<0.6.0',
 'tox>=3.20.1,<4.0.0',
 'twine>=3.2.0,<4.0.0',
 'wheel>=0.36.0,<0.37.0']

setup_kwargs = {
    'name': 'py-dev-deps',
    'version': '0.1.1',
    'description': 'A package for common python development dependencies',
    'long_description': "# py-dev-deps\n\nA project that only manages python development dependencies\n\nThe aim of this project is to provide a common denominator for python development dependencies\nin one package that can be added as a development dependency to other projects.  By using\npoetry to resolve and maintain a common set of compatible development dependencies, it may\nhelp to reduce the burdens of package installations for projects using this project as a\ndevelopment dependency.\n\n## Install\n\nSee [INSTALL](INSTALL.md) for more details; the following should work; note that\nthe intention is to use this package only for development dependencies.\n\n#### poetry\n\n```sh\npoetry add -D 'py-dev-deps'\n```\n\n#### pip\n\n```sh\ncat >> dev-requirements.txt <<EOF\npy-dev-deps\nEOF\n\npip install -r dev-requirements.txt\n```\n",
    'author': 'Darren Weber',
    'author_email': 'dweber.consulting@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dazza-codes/py-dev-deps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
