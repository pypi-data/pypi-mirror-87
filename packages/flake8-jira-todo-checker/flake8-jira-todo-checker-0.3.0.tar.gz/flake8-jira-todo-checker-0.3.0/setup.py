# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_jira_todo_checker']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3,<4', 'jira>=2.0.0,<3.0.0']

entry_points = \
{'flake8.extension': ['JIR = flake8_jira_todo_checker:Checker']}

setup_kwargs = {
    'name': 'flake8-jira-todo-checker',
    'version': '0.3.0',
    'description': 'Flake8 plugin to check that every TODO, FIXME, QQ etc comment has a JIRA ID next to it.',
    'long_description': "Flake8 JIRA TODO Checker\n========================\n\n[![CircleCI](https://circleci.com/gh/SimonStJG/flake8-jira-todo-checker/tree/master.svg?style=shield)](https://circleci.com/gh/SimonStJG/flake8-jira-todo-checker/tree/master)\n[![PyPI](https://img.shields.io/pypi/v/flake8-jira-todo-checker.svg?color=green)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/l/flake8-jira-todo-checker.svg?color=green)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/pyversions/flake8-jira-todo-checker.svg)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n[![PyPI](https://img.shields.io/pypi/format/flake8-jira-todo-checker.svg)](https://pypi.python.org/pypi/flake8-jira-todo-checker)\n\nFlake8 plugin to check that:\n\n 1. Every `TODO`, `FIXME`, `QQ` etc comment has a JIRA ID next to it.  \n 2. Every JIRA ID refers to a JIRA card which is not closed.\n\nIn other words, this is valid as long as the JIRA card ABC-123 is not closed:\n\n```\ndef hacky_function():\n    # TODO ABC-123 Stop reticulating splines\n    ...\n```\n\nBut this would raise the new flake8 error `JIR001`:\n\n```\ndef hacky_function():\n    # TODO Stop reticulating splines\n    ...\n```\n\n## Configuration\n\n### jira-project-ids\n\nA list of valid JIRA project IDs can be provided via the flag `--jira-project-ids` or via the key `jira-project-ids`\nin a flake8 configuration file, e.g\n\n```\njira-project-ids = ABC,DEF\n```\n\nIf no project IDs are provided then all TODOs will be rejected.\n\n### todo-synonyms\n\nA list of words which will be treated like TODO can be provided via the flags `--allowed-todo-synonyms` and \n`--disallowed-todo-synonyms` or via the key `allowed-todo-synonyms` and `disallowed-todo-synonyms` in a flake8 \nconfiguration file.  \n\n`disallowed-todo-synonyms` will raise an error whenever found in the codebase, and `allowed-todo-synonyms` will raise an \nerror only if it's missing a JIRA card or that JIRA card is invalid.\n\nDefaults to:\n```\nallowed-todo-synonyms = TODO\ndisallowed-todo-synonyms = FIX,QQ\n```\n\n### jira-server\n\nThe URL of the JIRA server, if unset the status of JIRA cards won't be checked.\n\n\n### disallowed-jira-statuses, disallowed-jira-resolutions, and disallow-all-jira-resolutions\n\nIf a TODO is attached to a JIRA issue whose status is in `disallowed-jira-statuses` then an error will be reported, \nditto if the JIRA card has a resolution in `disallowed-jira-resolutions`.  If `disallow-all-jira-resolutions` is set to \n`True`, then report an error if issue has any resolution. \n\nDefaults to:\n```\ndisallowed-jira-statuses = Done\ndisallow-all-jira-resolutions = True\n```\n\n### JIRA Authentication\n\nWe support the same authentication methods as the \n[jira-python](https://jira.readthedocs.io/en/master/examples.html#authentication) library.\n\nFor cookie-based username/password authentication, use the following configuration parameters:\n\n1.  `jira-cookie-username`\n1.  `jira-cookie-password`\n\nFor HTTP Basic username/password authentication, use the following configuration parameters:\n\n1.  `jira-http-basic-username`\n1.  `jira-http-basic-password`\n\nFor OAuth authentication, use the following configuration parameters:\n\n1.  `jira-oauth-access-token`\n1.  `jira-oauth-access-token-secret`\n1.  `jira-oauth-consumer-key`\n1.  `jira-oauth-key-cert-file`\n\nFor kerberos authentication, set the `jira-kerberos` configuration parameter to True. \n\n## Alternatives\n\nThis project is heavily inspired by the [Softwire TODO checker](https://github.com/Softwire/todo-checker).\n\n## Releasing\n\n1. `poetry run bump2version minor`\n1. `git push && git push --tags`\n1. `tox -e pypi`\n\n# TODO\n\nTest and add instructions for JIRA cloud.",
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
