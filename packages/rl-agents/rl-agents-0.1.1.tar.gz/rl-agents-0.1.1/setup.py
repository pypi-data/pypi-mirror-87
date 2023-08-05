# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rl_agents',
 'rl_agents.agents',
 'rl_agents.agents.functions',
 'rl_agents.agents.mab',
 'rl_agents.agents.policies',
 'rl_agents.agents.tabular',
 'rl_agents.envs',
 'rl_agents.runners']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.17.2,<0.18.0', 'numpy>=1.18.4,<2.0.0', 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'rl-agents',
    'version': '0.1.1',
    'description': 'Implementation of various reinforcement learning methods.',
    'long_description': "=========\nRL-Agents\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/rl-agents.svg\n        :target: https://pypi.python.org/pypi/rl-agents\n\n.. image:: https://travis-ci.org/mateuspontesm/rl-agents.svg?branch=master\n        :target: https://travis-ci.org/mateuspontesm/rl-agents\n        :alt: Travis-CI Build Status\n\n.. image:: https://readthedocs.org/projects/rl-agents/badge/?version=latest\n        :target: https://rl-agents.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://coveralls.io/repos/mateuspontesm/rl-agents/badge.svg?branch=master&service=github\n        :alt: Coverage Status\n        :target: https://coveralls.io/r/mateuspontesm/rl-agents\n\n.. image:: https://codecov.io/gh/mateuspontesm/rl-agents/branch/master/graphs/badge.svg?branch=master\n        :alt: Coverage Status\n        :target: https://codecov.io/github/mateuspontesm/rl-agents\n\n.. image:: https://img.shields.io/scrutinizer/quality/g/mateuspontesm/rl-agents/master.svg\n        :alt: Scrutinizer Status\n        :target: https://scrutinizer-ci.com/g/mateuspontesm/rl-agents/\n\n.. image:: https://codeclimate.com/github/mateuspontesm/rl-agents/badges/gpa.svg\n        :target: https://codeclimate.com/github/mateuspontesm/rl-agents\n        :alt: CodeClimate Quality Status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n        :target: https://github.com/ambv/black\n\nImplementation of various reinforcement learning methods.\n\n\n* Free software: BSD 3-Clause 'New' or 'Revised' License\n\n* Documentation: https://rl-agents.readthedocs.io.\n\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `mateuspontesm/cookiecutter-poetry`_ project template,\na fork of `johanvergeer/cookiecutter-poetry`_ project template\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`johanvergeer/cookiecutter-poetry`: https://github.com/johanvergeer/cookiecutter-poetry\n.. _`mateuspontesm/cookiecutter-poetry`: https://github.com/mateuspontesm/cookiecutter-poetry\n",
    'author': 'Mateus Mota',
    'author_email': 'mateuspontesm@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mateuspontesm/rl-agents',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
