# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_de_familia']

package_data = \
{'': ['*'],
 'py_de_familia': ['ativos-de-familia/boliviano/*',
                   'ativos-de-familia/jailson/*',
                   'ativos-de-familia/kauan-desu/*',
                   'ativos-de-familia/pau-guina/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'click_completion>=0.5.2,<0.6.0',
 'playsound>=1.2.2,<2.0.0',
 'pytest>=6.1.2,<7.0.0',
 'vext.gi>=0.7.4,<0.8.0',
 'vext>=0.7.4,<0.8.0']

entry_points = \
{'console_scripts': ['py-de-familia = '
                     'py_de_familia.clidefamilia:entrypoint_de_familia']}

setup_kwargs = {
    'name': 'py-de-familia',
    'version': '0.1.1',
    'description': 'CLI deliciosa de família',
    'long_description': '',
    'author': 'augustoliks',
    'author_email': 'carlos.neto.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/augustoliks/py-de-familia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
