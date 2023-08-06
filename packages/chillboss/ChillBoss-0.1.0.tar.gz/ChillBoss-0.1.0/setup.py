# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chillboss']

package_data = \
{'': ['*']}

install_requires = \
['PyAutogui>=0.9.50,<0.10.0', 'click>=7.1.2,<8.0.0', 'pyfiglet>=0.8.post1,<0.9']

setup_kwargs = {
    'name': 'chillboss',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'NaveenKumarReddy8',
    'author_email': 'mr.naveen8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
