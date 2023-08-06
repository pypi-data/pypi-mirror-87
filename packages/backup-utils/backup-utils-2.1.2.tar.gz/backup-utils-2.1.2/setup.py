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
    'version': '2.1.2',
    'description': 'The goal of the project is to simplify backup creation.',
    'long_description': 'Backup Utils\n============\n\n\n[![pipeline status](https://gitlab.com/Oprax/backup-utils/badges/master/pipeline.svg)](https://gitlab.com/Oprax/backup-utils/commits/master)\n[![coverage report](https://gitlab.com/Oprax/backup-utils/badges/master/coverage.svg)](https://gitlab.com/Oprax/backup-utils/commits/master)\n[![Documentation Status](https://readthedocs.org/projects/backup-utils/badge/?version=latest)](https://backup-utils.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - License](https://img.shields.io/pypi/l/backup-utils.svg)](https://gitlab.com/Oprax/backup-utils/blob/master/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/backup-utils.svg)](https://pypi.org/project/backup-utils/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/backup-utils.svg)](https://pypi.org/project/backup-utils/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\nThe goal of this project is to create a front to a backup program like Borg.\nIndeed, Borg is a really great tool for backup,\nbut I always write a bash script to specify directories I want to save.\nI also use Rclone to synchronize my backup to a remote.\nAnd finally, I need to backup my database.\n\nThere are three steps to backup :\n1. Database export\n2. Archiving\n3. Synchronize\n\nFor each step, you can use multiple drivers for multiple tools.\nAlso if something goes wrong, all Exceptions are catches to send a notification.\n\nBy default, database export use **mysql**, archiving **borg**, and synchronize **rclone**.\n\nVisit [documentation](https://backup-utils.readthedocs.io/) for more details.',
    'author': 'Romain Muller',
    'author_email': 'com@oprax.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Oprax/backup-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
