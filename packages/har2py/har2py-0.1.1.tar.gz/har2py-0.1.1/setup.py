# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['har2py']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0']

entry_points = \
{'console_scripts': ['har2py = har2py.main:cli']}

setup_kwargs = {
    'name': 'har2py',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'S1M0N38',
    'author_email': 'bertolottosimone@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
