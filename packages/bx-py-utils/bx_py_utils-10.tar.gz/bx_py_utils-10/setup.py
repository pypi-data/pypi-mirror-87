# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bx_py_utils', 'bx_py_utils.models', 'bx_py_utils.test_utils']

package_data = \
{'': ['*'],
 'bx_py_utils': ['locale/de/LC_MESSAGES/*', 'locale/en/LC_MESSAGES/*']}

install_requires = \
['django']

entry_points = \
{'console_scripts': ['publish = '
                     'bx_py_utils_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'bx-py-utils',
    'version': '10',
    'description': 'Various Python / Django utility functions',
    'long_description': '# Boxine - bx_py_utils\n\nVarious Python / Django utility functions\n\n## Quickstart\n\n```bash\npip install bx_py_utils\n```\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/bx_py_utils.git\n~$ cd bx_py_utils\n~/bx_py_utils$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\ntox-py36             Run pytest via tox with *python v3.6*\ntox-py37             Run pytest via tox with *python v3.7*\ntox-py38             Run pytest via tox with *python v3.8*\ntox-py39             Run pytest via tox with *python v3.9*\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nmakemessages         Make and compile locales message files\n```\n\n## License\n\n[MIT](LICENSE). Patches welcome!\n\n## Links\n\n* https://pypi.org/project/bx-py-utils/\n',
    'author': 'Jens Diemer',
    'author_email': 'jens.diemer@boxine.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0.0',
}


setup(**setup_kwargs)
