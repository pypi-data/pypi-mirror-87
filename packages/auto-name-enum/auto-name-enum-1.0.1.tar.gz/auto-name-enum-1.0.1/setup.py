# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_name_enum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'auto-name-enum',
    'version': '1.0.1',
    'description': 'String-based Enum class that automatically assigns values',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
