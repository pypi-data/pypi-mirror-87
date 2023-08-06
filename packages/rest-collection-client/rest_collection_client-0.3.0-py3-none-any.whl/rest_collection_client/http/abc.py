from abc import ABCMeta, abstractmethod
from asyncio import Lock, gather, wait
from typing import Any, Optional, Tuple, Union
from ujson import dumps

from aiohttp import ClientResponse, \
    ClientResponseError, ClientSession, ContentTypeError
from aiohttp.hdrs import METH_GET
from yarl import URL

from rest_collection_client.typing import JsonContentOrText
from .container import ClientResponseContextManager, HttpClientExcData
from .exc import AIOHTTP_EXCEPTION_MAP, HttpClientAuthenticationError, \
    HttpClientAuthorizationError, HttpClientRequestError, \
    HttpClientResponseContentError, HttpClientResponseError

__all__ = [
    'AbstractHttpClient',
    'AbstractGetHttpClient',
    'AbstractChunkedGetHttpClient',
    'AbstractAuthenticatedChunkedGetHttpClient'
]


def _remove_raise_for_status_param(params: dict):
    params.pop('raise_for_status', None)


class AbstractHttpClient(metaclass=ABCMeta):
    """Abstract class for http client."""

    def __init__(self, **session_params) -> None:
        # Delete raise for status option, handle statuses manualy.
        _remove_raise_for_status_param(session_params)

        self._session = ClientSession(json_serialize=dumps,
                                      raise_for_status=False,
                                      **session_params)

    async def close(self) -> None:
        await self._session.close()

    @abstractmethod
    async def get(self, url: str, *args, **kwargs) -> Any:
        """Get method."""

    @abstractmethod
    async def post(self, url: str, *args, data=None, **kwargs) -> Any:
        """Post method."""

    @abstractmethod
    async def put(self, url: str, *args, data=None, **kwargs) -> Any:
        """Put method."""

    @abstractmethod
    async def delete(self, url: str, *args, **kwargs) -> Any:
        """Delete method."""

    @abstractmethod
    async def options(self, url: str, *args, **kwargs) -> Any:
        """Options method."""

    async def __aenter__(self) -> 'AbstractHttpClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class AbstractGetHttpClient(AbstractHttpClient):
    """Abstract http client for GET requests only."""

    @abstractmethod
    async def get(self, url: str, *args, **kwargs) -> Any:
        pass

    async def options(self, url: str, *args, **kwargs):
        raise NotImplemented('GET client cannot perform OPTIONS requests.')

    async def post(self, url: str, *args, data=None, **kwargs):
        raise NotImplemented('GET client cannot perform POST requests.')

    async def put(self, url: str, *args, data=None, **kwargs):
        raise NotImplemented('GET client cannot perform PUT requests.')

    async def delete(self, url: str, *args, **kwargs):
        raise NotImplemented('GET client cannot perform DELETE requests.')


def _raise_for_status(resp: ClientResponse,
                      exc_data: Optional = None) -> None:
    """Raise for status wrapper."""
    try:
        resp.raise_for_status()

    except ClientResponseError as err:

        if resp.status == 401:
            raise HttpClientAuthenticationError(data=exc_data) from err

        elif resp.status == 403:
            raise HttpClientAuthorizationError(data=exc_data) from err

        raise HttpClientResponseContentError(data=exc_data) from err


class AbstractChunkedGetHttpClient(AbstractGetHttpClient):
    """Abstract http client for GET requests by chunks for performance and
    memory optimization purporses."""

    async def get(self,
                  url: str,
                  *args,
                  chunk_size: int = 100,
                  **kwargs) -> Tuple[JsonContentOrText, ...]:
        # Firstly, we should read first chunk, because we dont know how many
        # chunks should we request at all.
        first_chunk_url = self._compose_first_chunk_url(url, chunk_size)

        first_chunk = await self._get(first_chunk_url, *args, **kwargs)

        # We have first chunk, we can calculate other chunk urls by it`s
        # metadata.
        other_chunk_urls = self._compose_other_chunk_urls(
            url, chunk_size, first_chunk
        )

        get_chunk_coros = tuple(
            self._get(chunk_url, *args, **kwargs)
            for chunk_url in other_chunk_urls
        )
        gather_future = gather(*get_chunk_coros)

        try:
            return (first_chunk, *await gather_future)

        except Exception:
            # Exception occurs in one of coros, but other coros should be
            # cancelled and waited for ending.
            gather_future.cancel()
            await wait(get_chunk_coros)

            raise

    async def _request(self,
                       method: str,
                       url: Union[str, URL],
                       raise_for_status: bool = False,
                       **params) -> ClientResponse:

        try:
            return await self._session.request(
                method,
                url,
                raise_for_status=raise_for_status,
                **params,
            )

        except Exception as err:
            # todo: handle 401 and 403 statuses separately.
            exc_cls = AIOHTTP_EXCEPTION_MAP.get(
                type(err), HttpClientRequestError
            )
            raise exc_cls(data=HttpClientExcData(url, method, params)) from err

    async def _get(self, url: str, *args, **params) -> JsonContentOrText:
        _remove_raise_for_status_param(params)

        with ClientResponseContextManager(
            await self._request(METH_GET, url, raise_for_status=False, **params)
        ) as resp:

            exc_data = HttpClientExcData(url, METH_GET, params)
            _raise_for_status(resp, exc_data)

            try:
                content_type = resp.headers.get('content-type')

                if content_type is None:
                    return await resp.read()

                # https://www.ietf.org/rfc/rfc2045.txt
                # Content Type string can contain additional params like charset
                if content_type.startswith('application/json'):
                    # Server responsed with json, let's read it.
                    return await resp.json()

                if content_type.startswith('text/'):
                    # Server responsed with text, let's read it.
                    return await resp.text()

                return await resp.read()

            except ContentTypeError as err:
                raise HttpClientResponseError(data=exc_data) from err

            except Exception as err:
                raise HttpClientResponseContentError(data=exc_data) from err

    @abstractmethod
    def _compose_other_chunk_urls(self,
                                  url: str,
                                  chunk_size: int,
                                  first_chunk: JsonContentOrText) -> str:
        """Generate urls to request other chunks."""

    @abstractmethod
    def _compose_first_chunk_url(self,
                                 url: str,
                                 chunk_size: int) -> str:
        """Generate first chunk url."""


class AbstractAuthenticatedChunkedGetHttpClient(AbstractChunkedGetHttpClient):
    """Abstract class for http client for GET chunked requests with
    authentication."""

    def __init__(self, **session_params) -> None:
        super().__init__(**session_params)
        self._authenticated = False
        self._authenticated_lock = Lock()

    @abstractmethod
    def _compose_other_chunk_urls(self,
                                  url: str,
                                  chunk_size: int,
                                  first_chunk: JsonContentOrText) -> str: ...

    @abstractmethod
    def _compose_first_chunk_url(self,
                                 url: str,
                                 chunk_size: int) -> str: ...

    async def _check_authentication(self, authentication_data: Any) -> bool:
        """Checking authentication flag or get authentication."""
        async with self._authenticated_lock:
            if self._authenticated:
                return True

            # We cannot release lock, otherwise, anyone else can aquire this
            # lock again and check authentication, find, that it is
            # falsy, and start authentication request too.
            authenticated = await self._request_authentication(
                authentication_data
            )
            self._authenticated = authenticated
            return authenticated

    async def _clear_authentication(self) -> None:
        """Clear authentication flag and data."""
        async with self._authenticated_lock:
            await self._erase_authentication_data()
            self._authenticated = False

    @abstractmethod
    async def _request_authentication(self, authentication_data: Any) -> bool:
        """Making authentication request."""

    @abstractmethod
    async def _erase_authentication_data(self) -> None:
        """Clear session authentication information."""

    # noinspection PyMethodOverriding
    async def _get(self,
                   url: str,
                   authentication_data: Any,
                   *args,
                   **params) -> JsonContentOrText:
        authenticated = await self._check_authentication(authentication_data)

        if not authenticated:
            raise HttpClientAuthenticationError(
                data=HttpClientExcData(url, METH_GET, params)
            )

        try:
            return await super()._get(url, *args, **params)

        except (HttpClientAuthenticationError, HttpClientAuthorizationError):
            # May be, authentication data was expired, but flag is set, we need
            # request authentication again.
            await self._clear_authentication()
            authenticated = await self._check_authentication(
                authentication_data
            )

            if not authenticated:
                raise

            # We cannot await coro again, thats why we didn`t assign
            # expression ``super()._get(url, *args, **kwargs)`` to variable
            # before try/except block.
            return await super()._get(url, *args, **params)
