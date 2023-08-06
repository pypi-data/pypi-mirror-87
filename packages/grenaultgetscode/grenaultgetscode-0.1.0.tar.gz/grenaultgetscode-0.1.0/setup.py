# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grenaultgetscode']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['getscode = '
                     'grenaultgetscode.script:get_url_and_print_status_code']}

setup_kwargs = {
    'name': 'grenaultgetscode',
    'version': '0.1.0',
    'description': 'Get the HTTP status code for an HTTP GET',
    'long_description': None,
    'author': 'Guillaume Renault',
    'author_email': 'me@grenault.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/guillaumerenault/grenaultgetscode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
