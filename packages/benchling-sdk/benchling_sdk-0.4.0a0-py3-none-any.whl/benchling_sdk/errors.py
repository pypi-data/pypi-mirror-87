from dataclasses import dataclass
import json
from json import JSONDecodeError
from typing import Any, Dict, MutableMapping, Optional

from benchling_api_client.models.async_task import AsyncTask
from benchling_api_client.models.status1 import Status1
from benchling_api_client.types import Response


@dataclass
class BenchlingError(Exception):
    """ An error resulting from communicating with the Benchling API. This could be an error returned from the
    API intentionally (e.g., 400 Bad Request) or an unexpected transport error (e.g., 502 Bad Gateway)

    The json attribute is present if the API response provided a deserializable JSON body as part of the
    error description. It will be None if the response could not be parsed as JSON.

    The content attribute is any unparsed content returned as part of the response body.
    """

    status_code: int
    headers: MutableMapping[str, str]
    # TODO BNCH-15416 Can OpenAPI provide a model for this that we can serialize?
    json: Optional[Dict[str, str]]
    content: Optional[bytes]

    @classmethod
    def from_response(cls, response: Response) -> "BenchlingError":
        json_body = _parse_error_body(response.content)
        return cls(
            status_code=response.status_code,
            headers=response.headers,
            json=json_body,
            content=response.content,
        )

    def __str__(self):
        message = self.json if self.json else self.content
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={message})"


@dataclass
class RegistrationError(Exception):
    """ An error relating to Benchling registration """

    message: Optional[str] = None
    errors: Optional[Dict[Any, Any]] = None
    task_status: Optional[Status1] = None

    @classmethod
    def from_task(cls, task: AsyncTask) -> "RegistrationError":
        return cls(message=task.message, errors=task.errors, task_status=task.status)

    def __str__(self):
        return repr(self)


def raise_for_status(response: Response) -> None:
    if response.status_code < 200 or response.status_code >= 300:
        raise BenchlingError.from_response(response)


def _parse_error_body(content: bytes) -> Optional[Dict[str, str]]:
    if content:
        string_content = content.decode("utf-8")
        # In case the response is not a serialized JSON dict (e.g. a gateway error)
        try:
            return json.loads(string_content)
        except JSONDecodeError:
            # Some responses may not be JSON. Just catch the error
            return None
    return None
