# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dovado_rtl',
 'dovado_rtl.antlr',
 'dovado_rtl.antlr.generated',
 'dovado_rtl.antlr.generated.SysVerilogHDL',
 'dovado_rtl.antlr.generated.Verilog2001',
 'dovado_rtl.antlr.generated.vhdl',
 'tcl',
 'verilog',
 'vhdl',
 'vivado_out',
 'xdc']

package_data = \
{'': ['*'],
 'dovado_rtl': ['.vscode/*'],
 'dovado_rtl.antlr': ['grammars/*', 'grammars/.antlr/*']}

install_requires = \
['BeautifulSoup4>=4.9.1,<5.0.0',
 'antlr4-python3-runtime>=4.8.0,<4.9.0',
 'importlib-resources>=3.3.0,<4.0.0',
 'lxml>=4.5.2,<5.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pathvalidate>=2.3.0,<3.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'pymoo>=0.4.2,<0.5.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scipy>=1.5.4,<2.0.0',
 'sklearn>=0.0,<0.1']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['dovado = dovado_rtl.main:main']}

setup_kwargs = {
    'name': 'dovado-rtl',
    'version': '0.2.12',
    'description': 'CLI tool for RTL Design Space Exploration on top of Vivado',
    'long_description': '\n\n# DoVado\n\nAdvanced Computer Architectures (ACA) Research project 2020.   \nA CLI tool for RTL Design Space Exploration on top of Vivado.   \n&ldquo;Do&rsquo; vado?&rdquo; is an italian slang expression for &ldquo;Dove vado?&rdquo; which means &ldquo;Where do I go?&rdquo;\n\n\n# State of the Project\n\nComplete prototype.\n\n\n# How to inspect the project\n\nThis project uses [Poetry](https://python-poetry.org/) for managing dependences and python versions in order to avoid conflicting versions on different machines.\nFollowing instructions are tested on a Linux machine but should work on OSX with minor (or none) modifications.\n\n\n## Install Poetry\n\n(if you already have poetry installed skip to the next section)   \nExecute the following command in a shell to install poetry\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nYou will find poetry in $HOME/poetry/.bin where $HOME is usually something like *home/your-user-name* (on Linux).\nTo check that everything went well run:\n\n    poetry --version\n\nIf this does not work add the poetry installation directory to the PATH ([instructions](https://docs.oracle.com/cd/E19062-01/sun.mgmt.ctr36/819-5418/gaznb/index.html) for Linux)\n\n\n## Run an example\n\nClone this repository to your local machine:\n\n    git clone  --recurse-submodules -j8 https://github.com/DPaletti/dovado.git\n\nNow position at the project root (from now on all commands assume you are at project root):\n\n    cd dovado\n\nInstall all the required dependences:\n\n    poetry install\n\nRun an example:\n\n    poetry run dovado < examples/input_files/input_rtl_vadd.txt\n\nDoing so all the program prompts are automatically answered with each line in input (one line = one answer), open it to see the answers.\nAfter all the vivado output you should see examples&rsquo; WNS (worst negative slack) and LUT (lookup table) percentage utilization\n\n\n# Testing\n\nIn order to run tests:\n\n    poetry run pytest\n\nAll tests will be ran and their respective outcome shown.   \nTests are managed through pytest which is used as a testing library and as a test runner. Functions which call Vivado are mocked through monkeypatch (from pytest).   \n\nA recap of test coverage can be read by:\n\n    cd html_cov/\n    firefox index.html\n\nif you do not have firefox installed any other browser will do.   \n\n\n# Report\nA full report of the activity conducted in developing Dovado and studying the RTL design space exploration problem can be read ([here](./dovado.pdf)).\n',
    'author': 'Daniele Paletti',
    'author_email': 'danielepaletti98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DPaletti/dovado',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
