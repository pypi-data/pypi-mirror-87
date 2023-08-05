# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_jira_todo_checker']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3,<4']

entry_points = \
{'flake8.extension': ['JIR001 = flake8_jira_todo_checker:Checker']}

setup_kwargs = {
    'name': 'flake8-jira-todo-checker',
    'version': '0.2.0',
    'description': 'Flake8 plugin to check that every TODO, FIXME, QQ etc comment has a JIRA ID next to it.',
    'long_description': 'Flake8 JIRA TODO Checker\n========================\n\n[![CircleCI](https://circleci.com/gh/SimonStJG/flake8-jira-todo-checker/tree/master.svg?style=shield)](https://circleci.com/gh/SimonStJG/flake8-jira-todo-checker/tree/master)\n[![PyPI](https://img.shields.io/pypi/v/flake8-jira-todo-checker.svg?color=green)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/l/flake8-jira-todo-checker.svg?color=green)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/pyversions/flake8-jira-todo-checker.svg)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/format/flake8-jira-todo-checker.svg)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n\nFlake8 plugin to check that every `TODO`, `FIXME`, `QQ` etc comment has a JIRA ID next to it.\n\nIn other words, this is valid:\n\n```\ndef hacky_function():\n    # TODO ABC-123 Stop reticulating splines\n    ...\n```\n\nBut this would raise the new flake8 error `JIR001`:\n\n```\ndef hacky_function():\n    # TODO Stop reticulating splines\n    ...\n```\n\n## Configuration\n\n### jira-project-ids\n\nA list of valid JIRA project IDs can be provided via the flag `--jira-project-ids` or via the key `jira-project-ids`\nin a flake8 configuration file, e.g\n\n```\njira-project-ids = ABC,DEF\n```\n\nIf no project IDs are provided then all TODOs will be rejected.\n\n### todo-synonyms\n\nA list of words which will be treated like TODO can be provided via the flag `--todo-synonyms` or via the key \n`todo-synonyms` in a flake8 configuration file.  Defaults to:\n```\ntodo-synonyms = TODO,FIX,QQ\n```\n',
    'author': 'Simon StJG',
    'author_email': 'Simon.StJG@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonstjg/flake8-jira-todo-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
