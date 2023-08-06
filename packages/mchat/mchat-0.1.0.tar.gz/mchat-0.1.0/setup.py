# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mchat']

package_data = \
{'': ['*']}

install_requires = \
['pycraft @ git+https://github.com/ammaraskar/pyCraft.git@master',
 'rich>=9.3.0,<10.0.0']

setup_kwargs = {
    'name': 'mchat',
    'version': '0.1.0',
    'description': 'A console chat client for most Minecraft server versions',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
