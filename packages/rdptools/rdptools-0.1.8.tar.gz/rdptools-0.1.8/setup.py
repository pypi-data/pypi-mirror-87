# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rdptools']

package_data = \
{'': ['*']}

install_requires = \
['geopandas',
 'office365-rest-client==2.3.0.1',
 'pandas',
 'python-dotenv>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'rdptools',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Baiyue Cao',
    'author_email': 'caobaiyue@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
