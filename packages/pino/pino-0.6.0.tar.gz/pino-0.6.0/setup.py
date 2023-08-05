# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pino']

package_data = \
{'': ['*']}

install_requires = \
['style>=1.1.6,<2.0.0']

entry_points = \
{'console_scripts': ['pino-pretty = pino.pretty_cli:main']}

setup_kwargs = {
    'name': 'pino',
    'version': '0.6.0',
    'description': 'Python json logger inspired by pino.js',
    'long_description': 'pino.py\n=======\n\n> **Json natural logger for python** inspired by [pino.js](https://github.com/pinojs/pino) :evergreen_tree:\n\n[![PyPI](https://img.shields.io/pypi/v/pino.svg)](https://pypi.org/project/pino/)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pino.svg)](https://pypi.python.org/pypi/pino)\n[![Build Status](https://travis-ci.com/CoorpAcademy/pino.py.svg?branch=master)](https://travis-ci.com/CoorpAcademy/pino.py)\n[![codecov](https://codecov.io/gh/CoorpAcademy/pino.py/branch/master/graph/badge.svg)](https://codecov.io/gh/CoorpAcademy/pino.py)\n\n> In building port of [pinojs](https://github.com/pinojs/pino) logging library to python :snake:\n\n:warning: This is a in building prototype, it\'s API is subject to change.\nA CHANGELOG will be introduced once it\'s stable enough and publicized.\nUse it at you own risk, but feel free to reach with an issue.\n\n\n## Basic Example\n\n```python\nfrom pino import pino\n\nlogger = pino(\n    bindings={"apptype": "prototype", "context": "main"}\n)\n\nlogger.info("Hello, I just started")\nlogger.debug({"details": 42}, "Some details that won\'t be seen")\n\nchild_logger = logger.child(context="some_job")\nchild_logger.info("Job started")\nchild_logger.info({"duration": 4012}, "Job completed %s", "NOW")\n\nlogger.info("Program completed")\n```\n\nWhich would output:\n```\n{"level": "info", "time": 1587740056952, "message": "Hello, I just started", "host": "SomeHost", "apptype": "prototype", "context": "main", "millidiff": 0}\n{"level": "info", "time": 1587740056952, "message": "Job started", "host": "SomeHost", "context": "some_job", "apptype": "prototype", "millidiff": 0}\n{"level": "info", "time": 1587740056952, "message": "Job completed NOW", "host": "SomeHost", "duration": 4012, "context": "some_job", "apptype": "prototype", "millidiff": 0}\n{"level": "info", "time": 1587740056952, "message": "Program completed", "host": "SomeHost", "apptype": "prototype", "context": "main", "millidiff": 0}\n```\n\n## API\n### pino() constructor arguments\n\n- `bindings`: meta attached to the messages by default\n- `level`: minimal level to output logs, _default to `info`_\n- `enabled`: is logger enabled, _default to true_\n- `millidiff`: whether a millidiff is added to message, `ms` since last message, _enabled by default_.\n- `stream` : stream to write logs to, default to `sys.stdout`\n- `dump_function`: function to be used to serialise object to JSON, _default `json.dumps`_\n- `messagekey`: key for message entry,  _default `message`_\n\n### pino logger instance\n- log methods: `critical`, `error`, `warn`, `info`, `debug`: (extra_bindings?), message, template value\n- `.level`: access or update current log level\n\n- `child(metas)`: create a child logger instance with new metas/bindings attached to it. (metas can be provided either as dict or kwargs)\n\n### Complex examples\n\nYou can see more detailed examples in the [**examples** folder](./examples), notably [complex.py](./examples/complex.py)\n\n## Development :hammer_and_wrench:\n\nThis library use [***Poetry***](https://python-poetry.org/) for management of the project, it\'s dependencies, build and else.\n\nYou can run test on all supported python version with `poetry run task test` (which will run `tox`),\nor you can run on your current python version with `poetry run task pytest`.\n',
    'author': 'Adrien Becchis',
    'author_email': 'adrien.becchis@coorpacademy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoorpAcademy/pino.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
