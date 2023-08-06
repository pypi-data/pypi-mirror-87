# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relycomply_cli']

package_data = \
{'': ['*'], 'relycomply_cli': ['gql/*']}

install_requires = \
['dephell>=0.8.3,<0.9.0',
 'fn_deps>=0.1.0,<0.2.0',
 'gql==3.0.0a1',
 'pygments-graphql>=1.0.0,<2.0.0',
 'pygments>=2.7.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'termcolor>=1.1.0,<2.0.0',
 'terminaltables>=3.1.0,<4.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['rely = relycomply_cli.cli:main']}

setup_kwargs = {
    'name': 'relycomply-cli',
    'version': '0.1.1',
    'description': 'The RelyComply Command Line Interface',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
