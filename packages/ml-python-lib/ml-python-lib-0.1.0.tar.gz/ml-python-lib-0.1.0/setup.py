# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_python_lib', 'ml_python_lib.import_data', 'ml_python_lib.preprocess']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.2,<4.0.0',
 'keyring>=21.5.0,<22.0.0',
 'tensorflow>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'ml-python-lib',
    'version': '0.1.0',
    'description': 'Machine Learning Library for tensorflow training algorithms',
    'long_description': None,
    'author': 'Tanguy Coatalem',
    'author_email': 'tanguy.coatalem@cogneed.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
