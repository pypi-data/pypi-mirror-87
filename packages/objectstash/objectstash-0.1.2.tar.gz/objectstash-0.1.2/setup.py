# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['objectstash']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.38,<2.0.0', 'loguru>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'objectstash',
    'version': '0.1.2',
    'description': 'A wrapper around object stores.',
    'long_description': None,
    'author': 'Ludwig Schmidt',
    'author_email': 'ludwigschmidt2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ludwigschmidt/objectstash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
