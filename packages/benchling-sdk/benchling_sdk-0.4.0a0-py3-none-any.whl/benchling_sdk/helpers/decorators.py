from functools import wraps

from benchling_sdk.helpers.retry_helpers import retry_method


def api_method(f):
    @wraps(f)
    @retry_method
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper
