# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['backup_utils',
 'backup_utils.databases',
 'backup_utils.notifiers',
 'backup_utils.syncs',
 'backup_utils.tasks']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'docker>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'backup-utils',
    'version': '2.0.2',
    'description': 'The goal of the project is to simplify backup creation.',
    'long_description': None,
    'author': 'Romain Muller',
    'author_email': 'com@oprax.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
