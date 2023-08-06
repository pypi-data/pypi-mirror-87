# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['turpy', 'turpy.io']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'turpy',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jose Beltran',
    'author_email': 'drjobel.connection@gmail.com',
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
