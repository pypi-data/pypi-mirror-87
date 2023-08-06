# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['garden', 'globe']

package_data = \
{'': ['*']}

install_requires = \
['blackopt', 'loguru']

setup_kwargs = {
    'name': 'globalgarden',
    'version': '0.1.0',
    'description': 'distributed non-differentiable optimization',
    'long_description': None,
    'author': 'Ilya Kamen',
    'author_email': 'ikamenshchikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
