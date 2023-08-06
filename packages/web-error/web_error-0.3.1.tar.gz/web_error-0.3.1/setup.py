# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web_error', 'web_error.handler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'web-error',
    'version': '0.3.1',
    'description': 'Web based error utils',
    'long_description': '# Web Errors v0.3.1\n[![image](https://img.shields.io/pypi/v/web_error.svg)](https://pypi.org/project/web_error/)\n[![image](https://img.shields.io/pypi/l/web_error.svg)](https://pypi.org/project/web_error/)\n[![image](https://img.shields.io/pypi/pyversions/web_error.svg)](https://pypi.org/project/web_error/)\n![style](https://github.com/EdgyEdgemond/web-error/workflows/style/badge.svg)\n![tests](https://github.com/EdgyEdgemond/web-error/workflows/tests/badge.svg)\n[![codecov](https://codecov.io/gh/EdgyEdgemond/web-error/branch/master/graph/badge.svg)](https://codecov.io/gh/EdgyEdgemond/web-error)\n\n`web_error` is a set of exceptions and handlers for use in web apis to support easy error management and responses\n\nEach exception easily marshals to JSON for use in api errors. Handlers for different web frameworks are provided.\n\n\n## Errors\n\nThe base `web_error.error.HttpException` accepts a `message`, `debug_message`, `code` and `status` (default 500)\n\nAnd will render a response with status as the status code:\n\n```json\n{\n    "code": "code",\n    "message": "message",\n    "debug_message": "debug_message",\n}\n```\n\nSome convenience Exceptions are provided, to create custom error subclass these\nand define `message` and `code` attributes.\n\n* `web_error.error.ServerException` provides status 500 errors\n* `web_error.error.BadRequestException` provides status 400 errors\n* `web_error.error.UnauthorisedException` provides status 401 errors\n* `web_error.error.NotFoundException` provides status 404 errors\n\n### Custom Errors\n\nSubclassing the convenience classes provide a simple way to consistently raise the same error\nand message.\n\nCode is an optional attribute to provide a unique value to parse in a frontend/client instead of\nmatching against messages.\n\n```python\nfrom web_error.error import NotFoundException\n\n\nclass UserNotFoundError(NotFoundException):\n    message = "User not found."\n    code = "E001"\n```\n\n## Pyramid\n\nInclude the pyramid exception handlers in your config.\n\n```python\ndef main(global_config, **config_blob):\n    config = Configurator(settings=config_blob)\n\n    ...\n\n    config.scan("web_error.handler.pyramid")\n\n    return config.make_wsgi_app()\n```\n\nThis will handle all unexpected errors, and any app specific errors.\n\n```python\n@view_config(route_name="test", renderer="json")\ndef test(request):\n    raise UserNotFoundError("debug message")\n```\n\n\n## Flask\n\nRegister the error handler with your application\n\n```python\napp.register_error_handler(Exception, web_error.handler.flask.exception_handler)\n```\n\n## Aiohttp\n\nDecorate your views with the error handler.\n\n```python\n@web_error.handler.aiohttp.view_error_handler\nasync def user(self):\n    raise UserNotFoundError("debug message")\n```\n',
    'author': 'Daniel Edgecombe',
    'author_email': 'edgy.edgemond@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EdgyEdgemond/web-error/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
