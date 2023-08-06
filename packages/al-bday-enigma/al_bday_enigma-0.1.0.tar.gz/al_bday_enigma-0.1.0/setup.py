# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['al_bday_enigma']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.62.0,<0.63.0', 'royalnet==6.0.0a16', 'uvicorn>=0.12.3,<0.13.0']

setup_kwargs = {
    'name': 'al-bday-enigma',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
