# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['p360_contact_manager',
 'p360_contact_manager.api',
 'p360_contact_manager.usecases']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'dependencies>=2.0.0,<3.0.0',
 'iso3166>=1.0,<2.0',
 'requests>=2.24.0,<3.0.0',
 'returns>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['p360 = p360_contact_manager.cli:main']}

setup_kwargs = {
    'name': 'p360-contact-manager',
    'version': '1.2.0',
    'description': 'Public 360 application by Tieto has some issues with for example duplicated contacts. This package tries to fix that and adds other functionality like synchronization(enrichment) with brreg.no.',
    'long_description': '![test](https://github.com/greenbird/p360-contact-manager/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/greenbird/p360-contact-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbird/p360-contact-manager)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n# P360 Contact Manager\n\n**[Documentation](https://greenbird.github.io/p360-contact-manager/) |\n[Source Code](https://github.com/greenbird/p360-contact-manager) |\n[Task Tracker](https://github.com/greenbird/p360-contact-manager/issues)**\n\nWhile there are existing solutions to synchronize with systems such as brønnøysundregisteret. They can be used via GUI only and are slow to enrich and update the data. Some of the tools can create duplicates that are not accepted among all the systems.\n\nThis project addresses the following issues:\n\n* Creates simple and easy to use CLI interface\n* Runs faster than existing solutions\n* Removes duplicates\n* Multi-platform\n\n\n## Quickstart\n\nInstalling the package\n> `p360-contact-manager` is on [pypi](https://pypi.org/project/p360-contact-manager/) and can be installed with pip\n\n```sh\npip install p360-contact-manager\n```\n\nThis installs the `p360` CLI command. If you have installed it in a virtualenv, then remember to activate it before usng `p360`. If you have used `poetry` to install it, run it with `poetry run p360`.\n\n\n!!! note\n    In the examples replace `your_key` with your api authkey and `your_url` with the url to your api.\n\n\nStart with testing the connection\n```sh\np360 --authkey your_key --p360_base_url your_url test\n```\n\n\nFind duplicates\n```sh\np360 --authkey your_key --p360_base_url your_url duplicates\n```\n> Check the file `duplicate_worklist.json` thats created if everything looks okay. The filename can also be configured by using `--output my_duplicate_worklist.json`.\n\nRun update\n```sh\np360 -ak your_key -pbu your_url --worklist duplicates_worklist.json update\n```\n\nThis creates a file called `result_update.json` in your current working directory. This file contains a list of all enterprises which have been updated by recno. If there are any errors then those can be found in the same file with an error message and the payload that caused the error.\n',
    'author': 'Thomas Borgen',
    'author_email': 'thomas.borgen@greenbird.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/p360-contact-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
