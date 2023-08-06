# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ratelimit', 'ratelimit.auths', 'ratelimit.backends']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6,<0.7'],
 'full': ['aredis>=1.1.8,<2.0.0', 'pyjwt>=1.7.1,<2.0.0'],
 'jwt': ['pyjwt>=1.7.1,<2.0.0'],
 'redis': ['aredis>=1.1.8,<2.0.0']}

setup_kwargs = {
    'name': 'asgi-ratelimit',
    'version': '0.4.0',
    'description': '',
    'long_description': '# ASGI RateLimit\n\nLimit user access frequency. Base on ASGI.\n\n100% coverage. High performance. Support regular matching. Customizable.\n\n## Install\n\n```\n# Only install\npip install asgi-ratelimit\n\n# Use redis\npip install asgi-ratelimit[redis]\n\n# Use jwt\npip install asgi-ratelimit[jwt]\n\n# Install all\npip install asgi-ratelimit[full]\n```\n\n## Usage\n\nThe following example will limit users under the `"default"` group to access `/second_limit` at most once per second and `/minute_limit` at most once per minute. And the users in the `"admin"` group have no restrictions.\n\n```python\nfrom typing import Tuple\n\nfrom ratelimit import RateLimitMiddleware, Rule\nfrom ratelimit.auths import EmptyInformation\nfrom ratelimit.backends.redis import RedisBackend\n\n\nasync def AUTH_FUNCTION(scope) -> Tuple[str, str]:\n    """\n    Resolve the user\'s unique identifier and the user\'s group from ASGI SCOPE.\n\n    If there is no user information, it should raise `EmptyInformation`.\n    If there is no group information, it should return "default".\n    """\n    return USER_UNIQUE_ID, GROUP_NAME\n\n\nrate_limit = RateLimitMiddleware(\n    ASGI_APP,\n    AUTH_FUNCTION,\n    RedisBackend(),\n    {\n        r"^/second_limit": [Rule(second=1), Rule(group="admin")],\n        r"^/minute_limit": [Rule(minute=1), Rule(group="admin")],\n    },\n)\n\n# Or in starlette/fastapi/index.py\napp.add_middleware(\n    RateLimitMiddleware,\n    authenticate=AUTH_FUNCTION,\n    backend=RedisBackend(),\n    config={\n        r"^/second_limit": [Rule(second=1), Rule(group="admin")],\n        r"^/minute_limit": [Rule(minute=1), Rule(group="admin")],\n    },\n)\n```\n\n### Block time\n\nWhen the user\'s request frequency triggers the upper limit, all requests in the following period of time will be returned with a `429` status code.\n\nExample: `Rule(second=5, block_time=60)`, this rule will limit the user to a maximum of 5 visits per second. Once this limit is exceeded, all requests within the next 60 seconds will return `429`.\n\n### Custom block handler\n\nJust specify `on_blocked` and you can customize the asgi application that is called when blocked.\n\n```python\nasync def yourself_429(scope: Scope, receive: Receive, send: Send) -> None:\n    await send({"type": "http.response.start", "status": 429})\n    await send({"type": "http.response.body", "body": b"429 page", "more_body": False})\n\n\nRateLimitMiddleware(..., on_blocked=yourself_429)\n```\n\n### Built-in auth functions\n\n#### Client IP\n\n```python\nfrom ratelimit.auths.ip import client_ip\n```\n\nObtain user IP through `scope["client"]` or `X-Real-IP`.\n\n#### Starlette Session\n\n```python\nfrom ratelimit.auths.session import from_session\n```\n\nGet `user` and `group` from `scope["session"]`.\n\nIf key `group` not in session, will return `default`. If key `user` not in session, will raise a `EmptyInformation`.\n\n#### Json Web Token\n\n```python\nfrom ratelimit.auths.jwt import create_jwt_auth\n\njwt_auth = create_jwt_auth("KEY", "HS256")\n```\n\nGet `user` and `group` from JWT that in `Authorization` header.\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/asgi-ratelimit',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
