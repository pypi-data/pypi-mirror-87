# Benchling SDK

A Python 3.8+ SDK for the [Benchling](https://www.benchling.com/) platform.

*Important!* This is an unsupported pre-release not suitable for production use.

## Getting Started

### Installation

Install the dependency via [Poetry](https://python-poetry.org/) (if applicable):

```bash
poetry add benchling-sdk
```
 
Or [Pip](https://pypi.org/project/pip/):
 
```bash
pip install benchling-sdk
```

### Using the SDK

Obtain a valid API key from your Benchling account and provide it to the SDK, along with the URL for the server.
Example:

```python
from benchling_sdk.benchling import Benchling
benchling = Benchling(url="https://my.benchling.com/api/v2", api_key="secure_api_key")
```

With `Benchling` now instantiated, make a sample call to all requests with the schema ID `assaych_test`:

```python
requests = benchling.requests.list_all("assaych_test")
```

In general, API calls are synchronous and blocking.

### Generators

Some methods which call paginated API endpoints will produce 
[Python generators](https://wiki.python.org/moin/Generators). Example:

```python
requests_generator = benchling.requests.list("assaych_test")
next_request = next(requests_generator)
```

### Error Handling

Failed API interactions will generally return a `BenchlingError`, which will contain some underlying
information on the HTTP response such as the status. Example:

```python
from benchling_sdk.errors import BenchlingError

try:
    requests = benchling.requests.list_all("assaych_test")
except BenchlingError as error:
    print(error.status_code)
```
