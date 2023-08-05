# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loadr']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=4.15.0,<5.0.0',
 'Jinja2>=2.11.2,<3.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.0,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['loadr = loadr.cli:main']}

setup_kwargs = {
    'name': 'loadr',
    'version': '0.1.6',
    'description': 'Simple tool to generate files based on Jinja2 templates and POST them to an API.',
    'long_description': None,
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
