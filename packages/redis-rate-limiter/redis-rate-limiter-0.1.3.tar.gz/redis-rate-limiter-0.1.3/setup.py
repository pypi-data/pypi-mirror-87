# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_rate_limiter']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redis-rate-limiter',
    'version': '0.1.3',
    'description': 'A Redis based rate limiter implementation for Python',
    'long_description': "# redis-rate-limiter\n\n## Install\n\n```bash\npip install -U redis-rate-limiter\n```\n\n## Use\n\n```python\nfrom redis_rate_limiter.config imoport basic_config\nfrom redis_rate_limiter.rate_limiter import RateLimiter\n\nbasic_config(redis_url='redis://localhost:6379/0')\n\n@RateLimiter(10, period=1)\ndef greet():\n    print('Hello')\n\nfor _ in range(100):\n    greet()\n\n# Raise RateLimitExceeded after print('Hello') 10 times\n```\n",
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
