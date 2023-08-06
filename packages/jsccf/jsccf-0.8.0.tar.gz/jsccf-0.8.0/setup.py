# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsccf']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jsccf = jsccf.jsccf:main']}

setup_kwargs = {
    'name': 'jsccf',
    'version': '0.8.0',
    'description': 'Renaming and documenting tool for JavaScript',
    'long_description': None,
    'author': 'Sergei',
    'author_email': 'isara.isara8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
