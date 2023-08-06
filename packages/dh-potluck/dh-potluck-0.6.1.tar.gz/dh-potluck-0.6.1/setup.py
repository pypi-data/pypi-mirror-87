# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dh_potluck', 'dh_potluck.celery', 'dh_potluck.utils']

package_data = \
{'': ['*'], 'dh_potluck': ['templates/*']}

install_requires = \
['Werkzeug>=0.15.0',
 'boltons>=19.1,<20.0',
 'ddtrace>=0.25.0',
 'flask-limiter>=1.2.1,<2.0.0',
 'flask>=1.0,<2.0',
 'flask_sqlalchemy>=2.4.4,<3.0.0',
 'json-log-formatter>=0.3.0,<0.4.0',
 'marshmallow>=2.19,<3.0',
 'requests>=2.22,<3.0',
 'sqlalchemy>=1.3,<2.0',
 'webargs>=5.5.2,<6.0.0']

setup_kwargs = {
    'name': 'dh-potluck',
    'version': '0.6.1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
