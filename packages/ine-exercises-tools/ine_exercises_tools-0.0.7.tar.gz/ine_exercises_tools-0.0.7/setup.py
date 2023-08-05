# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ine_exercises_tools']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.51,<2.0',
 'click>=7.1.2,<8.0.0',
 'colorful>=0.5.4,<0.6.0',
 'requests-toolbelt>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'ine-exercises-tools',
    'version': '0.0.7',
    'description': '',
    'long_description': None,
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
