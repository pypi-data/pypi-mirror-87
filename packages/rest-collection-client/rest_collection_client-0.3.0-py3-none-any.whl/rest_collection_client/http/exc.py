from asyncio import TimeoutError

from aiohttp import ClientConnectionError, ClientError, ClientPayloadError, \
    ClientResponseError, InvalidURL
from extra_collections import ExceptionMap

from rest_collection_client.exc import RestCollectionClientError

__all__ = [
    'HttpClientError',
    'HttpClientUrlError',
    'HttpClientRequestError',
    'HttpClientConnectionError',
    'HttpClientResponseError',
    'HttpClientResponseProtocolError',
    'HttpClientResponseContentError',
    'HttpClientAuthenticationError',
    'HttpClientAuthorizationError',
    'AIOHTTP_EXCEPTION_MAP',
]


class HttpClientError(RestCollectionClientError, ClientError):
    """Root http client exception."""


class HttpClientUrlError(HttpClientError, InvalidURL):
    """Http client invalid url error."""


class HttpClientRequestError(HttpClientError):
    """Http request error."""


class HttpClientConnectionError(HttpClientRequestError, ClientConnectionError):
    """Http client connection error."""


class HttpClientResponseError(HttpClientRequestError, ClientResponseError):
    """Http client response error."""


class HttpClientResponseProtocolError(HttpClientResponseError,
                                      ClientPayloadError):
    """Http client response protocol error."""


class HttpClientResponseContentError(HttpClientResponseError):
    """Http client response content error."""


class HttpClientAuthenticationError(HttpClientResponseContentError):
    """Http authentication error."""


class HttpClientAuthorizationError(HttpClientResponseContentError):
    """Http authorization error."""


AIOHTTP_EXCEPTION_MAP = ExceptionMap({
    ClientError: HttpClientError,
    InvalidURL: HttpClientUrlError,
    ClientConnectionError: HttpClientConnectionError,
    ClientResponseError: HttpClientResponseError,
    ClientPayloadError: HttpClientResponseProtocolError,
    # timeout sometimes raises ``asyncio.TimeoutError`` exception.
    TimeoutError: HttpClientConnectionError,
}, default_value=HttpClientError)
