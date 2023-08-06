# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_pony',
 'dj_pony.applied_migrations_checker',
 'dj_pony.applied_migrations_checker.management',
 'dj_pony.applied_migrations_checker.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.8']

setup_kwargs = {
    'name': 'dj-pony.applied-migrations-checker',
    'version': '0.1.3',
    'description': 'Check that all django database migrations have been applied.',
    'long_description': None,
    'author': 'Samuel Bishop',
    'author_email': 'sam@techdragon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
