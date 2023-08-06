# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['soft_collect',
 'soft_collect.db',
 'soft_collect.save',
 'soft_collect.templates',
 'soft_collect.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'cx_Oracle>=8.0.0,<9.0.0',
 'dynaconf>=3.0.0,<4.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pyodbc>=4.0.30,<5.0.0',
 'rich>=3.0.0,<4.0.0',
 'tucuxi>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['soft-collect = soft_collect.console:main']}

setup_kwargs = {
    'name': 'soft-collect',
    'version': '0.2.0',
    'description': 'Soft-Collect',
    'long_description': '\nsoft-collect\n============\n\n\n\n|PyPI|  |Black| |pre-commit|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/soft-collect.svg\n   :target: https://pypi.org/project/soft-collect/\n   :alt: PyPI\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *soft-collect* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install soft-collect\n\n\nUsage\n-----\n\n* TODO\n\n\n\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n',
    'author': 'Luccas Quadros',
    'author_email': 'luccas.quadros@softplan.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unj-inovacao/soft-collect',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
