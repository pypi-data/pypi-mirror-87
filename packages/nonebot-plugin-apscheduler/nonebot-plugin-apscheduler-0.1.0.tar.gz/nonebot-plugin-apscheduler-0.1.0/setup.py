# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_apscheduler']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.6.3,<4.0.0', 'nonebot2>=2.0.0-alpha.7,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-apscheduler',
    'version': '0.1.0',
    'description': 'APScheduler Support for NoneBot2',
    'long_description': None,
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
