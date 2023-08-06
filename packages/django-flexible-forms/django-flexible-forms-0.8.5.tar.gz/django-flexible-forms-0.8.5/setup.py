# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flexible_forms']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2',
 'jmespath>=0.10.0,<0.11.0',
 'requests>=2.24.0,<3.0.0',
 'simpleeval>=0.9.10,<0.10.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'django-flexible-forms',
    'version': '0.8.5',
    'description': 'A reusable Django app for managing database-backed forms.',
    'long_description': None,
    'author': 'Eric Abruzzese',
    'author_email': 'eric.abruzzese@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
