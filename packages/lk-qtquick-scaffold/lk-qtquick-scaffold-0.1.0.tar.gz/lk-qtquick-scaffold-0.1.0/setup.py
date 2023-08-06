# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_qtquick_scaffold',
 'lk_qtquick_scaffold.debugger',
 'lk_qtquick_scaffold.qml_helper']

package_data = \
{'': ['*'],
 'lk_qtquick_scaffold': ['theme/*',
                         'theme/Demo/*',
                         'theme/LightClean/*',
                         'theme/LightClean/LCBackground/*',
                         'theme/LightClean/LCButtons/*',
                         'theme/LightClean/LCStyle/*',
                         'theme/LightClean/rss/*']}

install_requires = \
['lk-logger>=3.6,<4.0', 'lk-utils>=1.4,<2.0', 'pyside2>=5.15,<6.0']

setup_kwargs = {
    'name': 'lk-qtquick-scaffold',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
