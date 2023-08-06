# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devcli', 'devcli_gitlab', 'devcli_npm_install', 'devcli_poetry_install']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'cachetools>=4.1.1,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'python-gitlab>=2.5.0,<3.0.0',
 'python-graphql-client>=0.4.0,<0.5.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['devcli = devcli:run']}

setup_kwargs = {
    'name': 'devcli',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Job de Noo',
    'author_email': 'jgdenoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devnoo/dev-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
