# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bx_py_utils',
 'bx_py_utils.approve_workflow',
 'bx_py_utils.dbperf',
 'bx_py_utils.models',
 'bx_py_utils.test_utils']

package_data = \
{'': ['*'],
 'bx_py_utils': ['locale/de/LC_MESSAGES/*', 'locale/en/LC_MESSAGES/*'],
 'bx_py_utils.approve_workflow': ['locale/de/LC_MESSAGES/*',
                                  'locale/en/LC_MESSAGES/*',
                                  'templates/approve_workflow/*']}

install_requires = \
['django']

entry_points = \
{'console_scripts': ['publish = '
                     'bx_py_utils_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'bx-py-utils',
    'version': '12',
    'description': 'Various Python / Django utility functions',
    'long_description': '# Boxine - bx_py_utils\n\nVarious Python / Django utility functions\n\n\n## Quickstart\n\n```bash\npip install bx_py_utils\n```\n\n\n## Existing stuff\n\nHere only a simple list about existing utilities.\nPlease take a look into the sources and tests for deeper informations.\n\n\n### models utilities\n\n* `approve_workflow` - Base model/admin/form classes to implement a model with draft/approve versions workflow\n* `manipulate.create_or_update()` - Similar to django\'s `create_or_update()` with benefits\n* `timetracking.TimetrackingBaseModel()` - Base model with "create" and "last update" date time\n\n\n### test utilities\n\n* `datetime.MockDatetimeGenerator()` - Mock django `timezone.now()` with generic time stamps\n* `datetime.parse_dt()` - Handy `datetime.strptime()` convert\n* `html_assertion.HtmlAssertionMixin` - Unittest mixin class with usefull assertments around Django test client tests\n* `model_clean_assert.CleanMock()` - Context manager to track if model `full_clean()` was called\n* `users` - Utilities around user/permission setup for tests\n\n### performance analysis\n* `dbperf.query_recorder.SQLQueryRecorder` - Context Manager that records SQL queries executed via the Django ORM\n\n### misc\n\n* `dict_utils.dict_get()` - nested dict `get()`\n* `dict_utils.pluck()` - Extract values from a dict, if they are present\n* `error_handling.print_exc_plus()` - Print traceback information with a listing of all the local variables in each frame\n* `filename.filename2human_name()` - Convert filename to a capitalized name\n* `filename.clean_filename()` - Convert filename to ASCII only via slugify\n* `stacktrace.get_stacktrace()` - Returns a filterable and easy-to-process stacktrace\n\n\n## developing\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/bx_py_utils.git\n~$ cd bx_py_utils\n~/bx_py_utils$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\ntox-py36             Run pytest via tox with *python v3.6*\ntox-py37             Run pytest via tox with *python v3.7*\ntox-py38             Run pytest via tox with *python v3.8*\ntox-py39             Run pytest via tox with *python v3.9*\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nmakemessages         Make and compile locales message files\nstart-dev-server     Start Django dev. server with the test project\nclean                Remove created files from the test project (e.g.: SQlite, static files)\n```\n\nYou can start the test project with the Django developing server, e.g.:\n```bash\n~/bx_py_utils$ make start-dev-server\n```\nThis is a own manage command, that will create migrations files from our test app, migrate, collectstatic and create a super user if no user exists ;)\n\nIf you like to start from stretch, just delete related test project files with:\n```bash\n~/bx_py_utils$ make clean\n```\n...and start the test server again ;)\n\n\n## License\n\n[MIT](LICENSE). Patches welcome!\n\n## Links\n\n* https://pypi.org/project/bx-py-utils/\n',
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
