# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hookers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hookers',
    'version': '1.0.0',
    'description': 'Python function call hookers',
    'long_description': '# hookers\nPython function call hookers\n',
    'author': '林玮 (Jade Lin)',
    'author_email': 'linw1995@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linw1995/hookers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
