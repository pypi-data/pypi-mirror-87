# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factfinder']

package_data = \
{'': ['*'], 'factfinder': ['data/*']}

install_requires = \
['cached-property==1.5.2',
 'census==0.8.15',
 'pandas==1.1.4',
 'python-dotenv==0.15.0',
 'typer==0.3.2']

setup_kwargs = {
    'name': 'pff-factfinder',
    'version': '0.0.0',
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
