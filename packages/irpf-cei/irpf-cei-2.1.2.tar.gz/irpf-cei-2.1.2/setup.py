# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['irpf_cei']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'inquirer>=2.6.3,<3.0.0',
 'pandas>=1.0.3,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['irpf-cei = irpf_cei.__main__:main']}

setup_kwargs = {
    'name': 'irpf-cei',
    'version': '2.1.2',
    'description': 'Programa auxiliar gratuito para calcular custos de ações, ETFs e FIIs.',
    'long_description': 'IRPF CEI\n========\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/irpf-cei.svg\n   :target: https://pypi.org/project/irpf-cei/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/irpf-cei\n   :target: https://pypi.org/project/irpf-cei\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/irpf-cei\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/irpf-cei/latest.svg?label=Read%20the%20Docs\n   :target: https://irpf-cei.readthedocs.io/\n   :alt: Read the documentation at https://irpf-cei.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/irpf-cei/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/irpf-cei/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/irpf-cei/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/irpf-cei\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nPrograma auxiliar para calcular custos de ações, ETFs e FIIs. Este programa foi feito para calcular emolumentos, taxa de liquidação e custo total para a declaração de Bens e Direitos do Imposto de Renda Pessoa Física.\n\n**Essa aplicação foi testada e configurada para calcular tarifas referentes ao ano de 2019-2020 (IRPF 2020) e não faz cálculos para compra e venda no mesmo dia (Day Trade), contratos futuros e Índice Brasil 50.**\n\n\nRequisitos\n----------\n\n1. Python\n\nInstale na sua máquina o Python 3.8.0 ou superior para o seu sistema operacional em python.org_.\n\nUsuários do Windows devem baixar a versão `Windows x86-64 executable installer` e na tela de instalação marcar a opção `Add Python 3.8 to PATH`:\n\n.. image:: docs/_images/winpath.png\n  :width: 400\n  :alt: Checkbox PATH na instalação Windows\n\n2. Suporte a língua Português (Brasil) no seu sistema operacional.\n\nPode ser instalado no Linux (Debian/Ubuntu) pelo comando:\n\n.. code:: console\n\n   $ apt-get install language-pack-pt-base\n\n\nInstalação\n----------\n\nYou can install *IRPF CEI* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install irpf-cei\n\n\nUso\n---\n\n1. Entre no `site do CEI`_, faça login e entre no menu Extratos e Informativos → Negociação de Ativos → Escolha uma corretora e as datas 1 de Janeiro e 31 de Dezembro do ano em que deseja declarar. Em seguida clique no botão “Exportar para EXCEL”. Ele irá baixar o arquivo “InfoCEI.xls”.\n2. Execute o programa através do comando:\n\n.. code:: console\n\n   $ irpf-cei\n\n\nO programa irá procurar o arquivo "InfoCEI.xls" na pasta atual (digite `pwd` no terminal para sabe qual é) ou na pasta downloads e exibirá na tela os resultados.\n\nAo executar, o programa pede para selecionar operações realizadas em leilão. Essa informação não pode ser obtida nos relatórios do CEI e precisam ser buscadas diretamente com a sua corretora de valores. Isso afeta o cálculo dos emolumentos e do custo médio.\n\n\nAviso legal (disclaimer)\n------------------------\n\nEsta é uma ferramenta com código aberto e gratuita, com licença MIT. Você pode alterar o código e distribuir, usar comercialmente como bem entender. Contribuições são muito bem vindas. Toda a responsabilidade de conferência dos valores e do envio dessas informações à Receita Federal é do usuário. Os desenvolvedores e colaboradores desse programa não se responsabilizam por quaisquer incorreções nos cálculos e lançamentos gerados.\n\n\n.. _python.org: https://www.python.org/downloads/\n.. _site do CEI: https://cei.b3.com.br/\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/irpf-cei',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
