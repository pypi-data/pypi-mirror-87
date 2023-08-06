from typing import Any, Coroutine, Optional

from aiohttp.hdrs import METH_DELETE, METH_GET, METH_HEAD, METH_OPTIONS, \
    METH_PATCH, METH_POST, METH_PUT
from aiohttp.typedefs import StrOrURL

__all__ = [
    'HttpClientGetMethodMixin',
    'HttpClientAllMethodsMixin',
]


class HttpClientGetMethodMixin:
    """HTTP client with GET method mixin."""
    def get(self,
            url: StrOrURL,
            *args: Any,
            **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP GET request."""
        return self._request(  # noqa
            METH_GET,
            url,
            *args,
            **kwargs,
        )


class HttpClientAllMethodsMixin(HttpClientGetMethodMixin):
    """HTTP client with all usable methods mixin."""
    def post(self,
             url: StrOrURL,
             *args: Any,
             data: Optional[Any] = None,
             **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP POST request."""
        return self._request(  # noqa
            METH_POST,
            url,
            *args,
            data=data,
            **kwargs,
        )

    def put(self,
            url: StrOrURL,
            *args: Any,
            data: Optional[Any] = None,
            **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP PUT request."""
        return self._request(  # noqa
            METH_PUT,
            url,
            *args,
            data=data,
            **kwargs,
        )

    def patch(self,
              url: StrOrURL,
              *args: Any,
              data: Optional[Any] = None,
              **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP PATCH request."""
        return self._request(  # noqa
            METH_PATCH,
            url,
            *args,
            data=data,
            **kwargs,
        )

    def delete(self,
               url: StrOrURL,
               *args: Any,
               **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP DELETE request."""
        return self._request(  # noqa
            METH_DELETE,
            url,
            *args,
            **kwargs,
        )

    def options(self,
                url: StrOrURL,
                *args: Any,
                **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP OPTIONS request."""
        return self._request(  # noqa
            METH_OPTIONS,
            url,
            *args,
            **kwargs,
        )

    def head(self,
             url: StrOrURL,
             *args: Any,
             **kwargs: Any) -> Coroutine[None, None, Any]:
        """HTTP HEAD request."""
        return self._request(  # noqa
            METH_HEAD,
            url,
            *args,
            **kwargs,
        )
