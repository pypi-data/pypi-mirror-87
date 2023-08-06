# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackopt',
 'blackopt.abc',
 'blackopt.algorithms',
 'blackopt.examples',
 'blackopt.examples.launchers',
 'blackopt.examples.problems',
 'blackopt.examples.problems.tsp',
 'blackopt.util']

package_data = \
{'': ['*'],
 'blackopt': ['blackopt.egg-info/*'],
 'blackopt.examples.launchers': ['_blackopt_workspace/reports/BumpyProblem 100 '
                                 '200@02-17_21-37-15/*',
                                 '_blackopt_workspace/reports/BumpyProblem 100 '
                                 '200@11-30_10-15-46/*']}

install_requires = \
['ilya-ezplot>=0.11,<0.12',
 'numpy>=1.18.1,<2.0.0',
 'pathos>=0.2.5,<0.3.0',
 'structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'blackopt',
    'version': '0.28',
    'description': 'black box optimization library',
    'long_description': None,
    'author': 'Ilya Kamen',
    'author_email': 'ikamenshchikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
