# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nata',
 'nata.backends',
 'nata.backends.osiris',
 'nata.plots',
 'nata.plots.types',
 'nata.plugins',
 'nata.plugins.grids',
 'nata.plugins.particles',
 'nata.plugins.plot',
 'nata.utils']

package_data = \
{'': ['*'], 'nata.plots': ['styles/*']}

install_requires = \
['h5py>=2.10.0,<3.0.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'matplotlib>=3.1.2,<4.0.0',
 'ndindex>=1.3.1,<2.0.0',
 'numpy>=1.18.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'docs': ['sphinx>=3.0.3,<4.0.0',
          'sphinx-rtd-theme>=0.4.3,<0.5.0',
          'recommonmark>=0.6.0,<0.7.0'],
 'wiptools': ['jupyterlab>=2.1.2,<3.0.0']}

setup_kwargs = {
    'name': 'nata',
    'version': '0.0.3',
    'description': 'Post-processing and visualization for PIC codes',
    'long_description': '<p align="center">\n     <img\n          src="https://raw.githubusercontent.com/GoLP-IST/nata/master/docs/_static/nata-logo.png"\n          alt="nata logo"\n          width=460\n     />\n</p>\n\n<p align="center">\n<a href="https://pypi.org/project/nata/"><img alt="PyPI" src="https://img.shields.io/pypi/v/nata"></a>\n<a href=\'https://nata.readthedocs.io/en/master/?badge=master\'>\n    <img src=\'https://readthedocs.org/projects/nata/badge/?version=master\' alt=\'Documentation Status\' />\n</a>\n</p>\n\n\n**Nata** is a python package for post-processing and visualizing simulation\noutput for particle-in-cell codes. It utilizes the numpy interface to provide\na simple way to read, manipulate, and represent simulation output.\n\n## Installing nata\n\nNata is available on PyPI. You can install it by running the following\ncommand inside your terminal\n\n```shell\npip install nata\n```\n\nIt can be used inside an IPython shell or [jupyter notebook](https://jupyter.org/) together\nwith [ipywidgets](https://github.com/jupyter-widgets/ipywidgets). Hence, you\nmight need to run after the installation\n\n```shell\n# can be skipped for notebook version 5.3 and above\njupyter nbextension enable --py --sys-prefix widgetsnbextension\n```\n\nand if you want to use it inside JupyterLab (note that this requires nodejs\nto be installed)\n\n```bash\njupyter labextension install @jupyter-widgets/jupyterlab-manager\n```\n\nIn case of issues, please visit the [installation section of ipywidgets](https://github.com/jupyter-widgets/ipywidgets/blob/master/docs/source/user_install.md)\nfor further details.\n\n## Contributing to nata\n\nAny type of contribution to nata is appreciated. If you have any issues,\nplease report them [by adding an issue on GitHub](https://github.com/GoLP-IST/nata/issues). But if\nyou wish to directly contribute to nata, we recommend to setup a local\ndevelopment environment. Follow the instruction below for more details.\n\n### Getting the source code\n\nThe source code is hosted on GitHub. Simply create a fork and apply your\nchanges. You can always push any changes to your local fork, but if you would\nlike to share your contribution, please create a pull request, so that it can\nbe reviewed.\n\n### Local Development Environment\n\nFor the local development environment, we use\n[poetry](https://python-poetry.org/). This allows us to deal better with\ndependencies issues and to ensure coding standards without the burden of\nmanually fixing and checking for styles. To use poetry, simply install it\nusing the latest version by running the following command in your terminal.\n\n```shell\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n```\n\nAfterwards, simply run\n\n```shell\npoetry install\n```\n\nwhich will install all the dependencies (including development packages) in a\nvirtual environment. If you wish to run a command inside the virtual\nenvironment, simply run it by `poetry run <your command>`, e.g. to run all\nthe test\n\n```shell\npoetry run pytest tests\n```\n\nAlternatively, you can directly use the virtual environment by running the\ncommand\n\n```shell\npoetry shell\n```\n\nwhich will spawn a shell inside the virtual environment. With this, you can\neven run jupyter outside of the source directory.\n\nIn addition, we use [pre-commit](https://pre-commit.com/) to help us keep\nconsistency in our development without any additional burden. Please use it\nas well. Inside the root directory of the repository, run the command\n\n```shell\npoetry run pre-commit install\n```\n\nwhich will create commit hooks for you and modify files keeping a consistent\nstructure.\n\n# Credits\n\n**Nata** is created and maintained by [Anton Helm](https://github.com/ahelm)\nand [Fábio Cruz](https://github.com/fabiocruz).\n\nThe development is kindly supported by the [Group for Lasers and Plasmas (GoLP)](http://epp.tecnico.ulisboa.pt/>).\n',
    'author': 'Anton Helm',
    'author_email': 'anton.helm@tecnico.ulisboa.pt',
    'maintainer': 'Anton Helm',
    'maintainer_email': 'anton.helm@tecnico.ulisboa.pt',
    'url': 'https://github.com/GoLP-IST/nata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
