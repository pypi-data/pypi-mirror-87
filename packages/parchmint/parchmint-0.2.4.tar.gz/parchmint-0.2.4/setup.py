# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parchmint']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0', 'jsonschema>=3.2.0,<4.0.0', 'networkx>=2.5,<3.0']

entry_points = \
{'console_scripts': ['parchmint-validate = parchmint.cmdline:validate_V1']}

setup_kwargs = {
    'name': 'parchmint',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'Radhakrishna Sanka',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
