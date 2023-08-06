# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchling_sdk',
 'benchling_sdk.helpers',
 'benchling_sdk.services',
 'benchling_sdk.services.inventory',
 'benchling_sdk.services.schema']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0', 'benchling-api-client==0.9.1a']

setup_kwargs = {
    'name': 'benchling-sdk',
    'version': '0.4.0a0',
    'description': 'SDK for interacting with the Benchling Platform. Currently unsupported for production use.',
    'long_description': '# Benchling SDK\n\nA Python 3.8+ SDK for the [Benchling](https://www.benchling.com/) platform.\n\n*Important!* This is an unsupported pre-release not suitable for production use.\n\n## Getting Started\n\n### Installation\n\nInstall the dependency via [Poetry](https://python-poetry.org/) (if applicable):\n\n```bash\npoetry add benchling-sdk\n```\n \nOr [Pip](https://pypi.org/project/pip/):\n \n```bash\npip install benchling-sdk\n```\n\n### Using the SDK\n\nObtain a valid API key from your Benchling account and provide it to the SDK, along with the URL for the server.\nExample:\n\n```python\nfrom benchling_sdk.benchling import Benchling\nbenchling = Benchling(url="https://my.benchling.com/api/v2", api_key="secure_api_key")\n```\n\nWith `Benchling` now instantiated, make a sample call to all requests with the schema ID `assaych_test`:\n\n```python\nrequests = benchling.requests.list_all("assaych_test")\n```\n\nIn general, API calls are synchronous and blocking.\n\n### Generators\n\nSome methods which call paginated API endpoints will produce \n[Python generators](https://wiki.python.org/moin/Generators). Example:\n\n```python\nrequests_generator = benchling.requests.list("assaych_test")\nnext_request = next(requests_generator)\n```\n\n### Error Handling\n\nFailed API interactions will generally return a `BenchlingError`, which will contain some underlying\ninformation on the HTTP response such as the status. Example:\n\n```python\nfrom benchling_sdk.errors import BenchlingError\n\ntry:\n    requests = benchling.requests.list_all("assaych_test")\nexcept BenchlingError as error:\n    print(error.status_code)\n```\n',
    'author': 'Benchling Customer Engineering',
    'author_email': 'ce-team@benchling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
