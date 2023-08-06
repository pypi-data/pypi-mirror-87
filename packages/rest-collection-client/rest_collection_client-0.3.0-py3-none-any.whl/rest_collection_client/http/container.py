from collections import namedtuple
from contextlib import AbstractContextManager

from aiohttp import ClientResponse

__all__ = [
    'ClientResponseContextManager',
    'HttpClientExcData',
]


class ClientResponseContextManager(AbstractContextManager):
    """``aiohttp.ClientResponse`` context manager."""
    def __init__(self, resp: ClientResponse) -> None:
        self._resp = resp

    def __enter__(self) -> ClientResponse:
        return self._resp

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._resp.release()


HttpClientExcData = namedtuple('HttpClientExcData', ('url', 'method', 'params'))
