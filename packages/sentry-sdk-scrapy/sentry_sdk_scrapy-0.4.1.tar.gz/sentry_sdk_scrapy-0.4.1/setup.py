# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentry_sdk_scrapy']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.4.1,<3.0.0', 'sentry-sdk>=0.19.4,<0.20.0']

setup_kwargs = {
    'name': 'sentry-sdk-scrapy',
    'version': '0.4.1',
    'description': 'Scrapy extension for integration of Sentry SDK to Scrapy projects',
    'long_description': '# scrapy-sentry-sdk\nA Scrapy extension for integration of Sentry SDK to Scrapy projects.\n\nThis package provides a Scrapy extension for convenient initialization of Sentry SDK.\n\n## Installation\n\n```shell script\npip install scrapy_sentry_sdk\n```\n\n## Usage\n\nTo use the extension add the following to you project `settings.py`:\n\n```python\n# Send exceptions to Sentry\n# replace SENTRY_DSN by you own DSN\nSENTRY_DSN = "XXXXXXXXXX"\n\n# Optionally, additional configuration options can be provided\nSENTRY_CLIENT_OPTIONS = {\n    "release": "you-project@version"  # these correspond to the sentry_sdk.init kwargs\n}\n\n# Enable or disable extensions\n# See https://doc.scrapy.org/en/latest/topics/extensions.html\nEXTENSIONS = {\n    \'scrapy_sentry_sdk.extensions.SentryLogging\': 1,  # Load SentryLogging extension before others\n}\n```\n\n## Configuration\n\nCurrently, this extension uses two Scrapy settings keys:\n\n- `SENTRY_DSN`: your project DSN (string, required)\n- `SENTRY_CLIENT_OPTIONS`: additional SDK options (dict, optional)\n\nMore details on configuring the SDK can be found in [Sentry documentation](https://docs.sentry.io/platforms/python/).\n',
    'author': 'KristobalJunta',
    'author_email': 'junta.kristobal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nouseforacode/scrapy-sentry-sdk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
