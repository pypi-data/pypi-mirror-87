# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcresult']

package_data = \
{'': ['*']}

install_requires = \
['deserialize>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'xcresult',
    'version': '0.1.0',
    'description': 'An xcresult parser.',
    'long_description': '# xcresult\n\n',
    'author': 'Dale Myers',
    'author_email': 'dale@myers.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dalemyers/xcresult',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
