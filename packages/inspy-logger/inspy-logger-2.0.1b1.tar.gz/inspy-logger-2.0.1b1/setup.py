# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspy_logger', 'inspy_logger.errors', 'inspy_logger.helpers']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=4.2.1,<5.0.0',
 'luddite>=1.0.1,<2.0.0',
 'packaging>=20.4,<21.0',
 'setuptools-autover>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'inspy-logger',
    'version': '2.0.1b1',
    'description': 'Colorable, scalable logger for CLI',
    'long_description': None,
    'author': 'Taylor-Jayde Blackstone',
    'author_email': 'tayjaybabee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
