# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_playground_attention']

package_data = \
{'': ['*']}

install_requires = \
['comet-ml>=3.2.7,<4.0.0',
 'nbdev>=1.1.5,<2.0.0',
 'tensorflow-gpu>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'ml-playground-attention',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cdfghglz',
    'author_email': 'cdfghglz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
