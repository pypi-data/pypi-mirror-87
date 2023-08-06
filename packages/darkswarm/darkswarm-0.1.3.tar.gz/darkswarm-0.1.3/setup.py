# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['darkswarm']

package_data = \
{'': ['*']}

install_requires = \
['docker[ssh]>=4.3.1,<5.0.0']

setup_kwargs = {
    'name': 'darkswarm',
    'version': '0.1.3',
    'description': 'Darkswarm is manual preload service/containers for docker swarm',
    'long_description': None,
    'author': 'Jeong Arm',
    'author_email': 'arm@gurum.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kjwon15/darkswarm/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
