# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['py-de-familia']

package_data = \
{'': ['*'],
 'py-de-familia': ['assets/boliviano/*',
                   'assets/jailson/*',
                   'assets/kauan-desu/*',
                   'assets/pau-guina/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'playsound>=1.2.2,<2.0.0',
 'vext.gi>=0.7.4,<0.8.0',
 'vext>=0.7.4,<0.8.0']

entry_points = \
{'console_scripts': ['py-de-familia = py_de_familia:main']}

setup_kwargs = {
    'name': 'py-de-familia',
    'version': '0.1.0',
    'description': 'CLI deliciosa',
    'long_description': '[![PyPI version](https://badge.fury.io/py/gelfguru.svg)](https://badge.fury.io/py/py-de-familia)\n\n\npy-de-familia\n=============\n\n.. raw:: html\n\n    <p align="center">\n        <a href="#readme">\n            <img alt="Loguru logo" src="docs/source/_static/logo.jpg">\n        </a>\n    </p>\n\n=========\n\n``py-de-familia`` é uma CLI deliciosa, criada no intuíto de relexar os programadores.\n\nNela é possível ouvir diretamente do seu terminal, as frases relexantes do mestre Jailson Mendes e dos personagens do universo PDF. \n\n.. raw:: html\n\n    <p align="center">\n        <a href="#readme">\n            <img alt="Loguru logo" src="docs/source/_static/jailson.gif">\n        </a>\n    </p>\n',
    'author': 'augustoliks',
    'author_email': 'carlos.santos110@fatec.sp.gov.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/augustoliks/py-de-familia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
