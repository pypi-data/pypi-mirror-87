# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fairtorch']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'fairtorch',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Masashi Sode',
    'author_email': 'masashi.sode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
