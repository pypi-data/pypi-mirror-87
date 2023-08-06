# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinger_demo']

package_data = \
{'': ['*']}

install_requires = \
['pystray==0.17.2', 'python-xlib==0.29', 'six==1.15.0']

extras_require = \
{':python_version >= "3.6"': ['Pillow>=8.0,<9.0']}

setup_kwargs = {
    'name': 'pinger-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alex Duki',
    'author_email': 'aleksey.duki.ext@nokia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
}


setup(**setup_kwargs)
