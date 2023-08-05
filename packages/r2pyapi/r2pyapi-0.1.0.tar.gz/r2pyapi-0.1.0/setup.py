# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['r2pyapi']

package_data = \
{'': ['*']}

install_requires = \
['r2pipe>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'r2pyapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Koh M. Nakagawa',
    'author_email': 'tsunekou1019@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
