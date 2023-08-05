# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transformers']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.4,<2.0.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'ku-transformers',
    'version': '1.0.3',
    'description': 'Ku exam transformer',
    'long_description': None,
    'author': 'Cesar Juarez',
    'author_email': 'cesaripn2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
