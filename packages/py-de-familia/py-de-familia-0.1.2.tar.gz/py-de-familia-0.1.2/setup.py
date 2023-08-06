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
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest>=6.1.2,<7.0.0',
 'vext.gi>=0.7.4,<0.8.0',
 'vext>=0.7.4,<0.8.0']

entry_points = \
{'console_scripts': ['py-de-familia = '
                     'py_de_familia.clidefamilia:entrypoint_de_familia']}

setup_kwargs = {
    'name': 'py-de-familia',
    'version': '0.1.2',
    'description': 'CLI deliciosa de família',
    'long_description': '.. image:: https://github.com/augustoliks/py-de-familia/blob/main/docs/source/_static/logo-with-desc.png?raw=true\n\n.. image:: https://badge.fury.io/py/py-de-familia.svg\n    :target: https://badge.fury.io/py/py-de-familia\n\n.. image:: https://readthedocs.org/projects/py-de-familia/badge/?version=latest\n    :target: https://py-de-familia.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://app.codacy.com/project/badge/Grade/2f6923d397794cec937347e9c792d1dc\n    :target: https://www.codacy.com/gh/augustoliks/py-de-familia/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=augustoliks/py-de-familia&amp;utm_campaign=Badge_Grade\n\n.. image:: https://img.shields.io/badge/license-APAICHE--DE--FAMILIA--2.0-blue\n    :target: https://github.com/augustoliks/py-de-familia/blob/main/LICENSE-DE-FAMILIA\n\n.. image:: https://codecov.io/gh/augustoliks/py-de-familia/branch/main/graph/badge.svg?token=EHJKGJKW3T\n    :target: https://codecov.io/gh/augustoliks/py-de-familia\n\n.. image:: https://travis-ci.com/augustoliks/py-de-familia.svg?branch=main\n    :target: https://travis-ci.com/github/augustoliks/py-de-familia\n\n=========\n\nÉ Essa Biblioteca Que Você Queria???\n====================================\n\n``py-de-família`` é uma CLI deliciosa, criada no intuíto de relaxar os Programadores de Família.\n\nNela é possível ouvir diretamente do seu terminal, as frases relexantes do mestre Jailson Mendes e de outros personagens do universo PDF.\n\n.. end-of-readme-intro\n\n*Features* de Família\n=====================\n\nAtualmente, é possível apreciar os aúdios relexantes dos seguintes personagens de família:\n\n+-------------------------------+----------------------------------+--------------------------------------------------------+\n| Personagem de Família         | Filmes de Família                | Biografia de Família                                   |\n+===============================+==================================+========================================================+\n| Jailson Mendes de Família     | Trilogia Pai de Família          | https://desciclopedia.org/wiki/Pai_de_Fam%C3%ADlia     |\n+-------------------------------+----------------------------------+--------------------------------------------------------+\n| Kauan Desu de Família         | Trilogia Pai de Família          | https://desciclopedia.org/wiki/Kauan_Desu              |\n+-------------------------------+----------------------------------+--------------------------------------------------------+\n| Paulo Guina de Família        | Trilogia Pai de Família          | https://desciclopedia.org/wiki/Paulo_Guina             |\n+-------------------------------+----------------------------------+--------------------------------------------------------+\n| Boliviano de Família          | Princesa Demacol e o Boliviano   | http://desciclo.pedia.ws/wiki/Boliviano                |\n+-------------------------------+----------------------------------+--------------------------------------------------------+\n\nInstalação\n==========\n\n.. code-block:: shell\n\n    # Instalação da biblioteca de familia\n    $ pip3 install py-de-familia\n\n    # Habilitando o autocomplete de familia\n    $ eval "$(_PY_DE_FAMILIA_COMPLETE=source_bash py-de-familia)"\n\nExecução\n========\n\nTODO\n\nEstrutura do Projeto de Família\n===============================\n\n::\n\n    ├── CODE-OF-CONDUCT-DE-FAMILIA.rst  # Código de conduta de Família\n    ├── docs                            # Documentação de Família\n    │   └── ...\n    ├── LICENSE-DE-FAMILIA              # Descrição da Licença APAICHE-DE-FAMILIA-2.0\n    ├── Makefile                        # Makefile de Família para extrair audios de família do youtube\n    ├── poetry.lock                     # Dependencias de Família Versionadas\n    ├── py_de_familia\n    │   ├── ativos-de-familia\n    │   │   ├── boliviano               # Audios do Boliviano de Família\n    │   │   │   └── ...\n    │   │   ├── jailson                 # Audios do Jailson Mendes de Família\n    │   │   │   └── ...\n    │   │   ├── kauan-desu              # Audios do Kauan Desu de Família\n    │   │   │   └── ...\n    │   │   └── pau-guina               # Audios do Paulo Guina de Família\n    │   │       └── ...\n    │   ├── autocomplete-de-familia.sh  # Shell Script Para habilitar o auto-complete\n    │   └── clidefamilia.py             # Código Fonte de Família\n    ├── pyproject.toml                  # Metadados do projeto de família\n    ├── README.rst                      # Documentação de família\n    └── tests                           # Testes de Família\n        ├── __pycache__\n        └── test_clidefamilia.py        # Testes unitários de Família, que seja pequeneninho mais que seja garantido\n\nLicença de Família\n==================\n\n``py-de-família`` é uma biblioteca *open-source*. Todo o desenvolvimento foi feito sobre a Licença **APAICHE-DE-FAMILIA-2.0**.\n\nEssa licença, tem como restrição, o tipo do Desenvolvedor atuante no projeto. É aceito apenas:\n\n* Héteros;\n* Machos;\n* Ursos; e\n* Lolitos.\n\nEsta é baseada nas licenças **PAPAKU** e **KUKÉPAU**, criadas respectivamente nas cidades de **Cú Pequeno** e **Pau Grande**.\n\nContribuições de Família\n========================\n\nPara contribuir com o código fonte, é necessário seguir o Código de Conduta deste projeto.\n\nPara adicionar mais audios relexantes, basta utilizar o ``Makefile`` de familia. Este tem seções que utilizam os utilitários ``youtube-dl`` e ``ffmpeg`` para baixar e converter os audios respectivamente.\n',
    'author': 'augustoliks',
    'author_email': 'carlos.neto.dev@gmail.com',
    'maintainer': 'augustoliks',
    'maintainer_email': 'carlos.neto.dev@gmail.com',
    'url': 'https://github.com/augustoliks/py-de-familia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
