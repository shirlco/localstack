import logging
import threading
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment, StartResponse

from werkzeug.datastructures import Headers
from werkzeug.wrappers import Request

from localstack.http import Response

from ..gateway import Gateway

LOG = logging.getLogger(__name__)


class WsgiGateway:
    """
    Exposes a Gateway as a WSGI application.
    """

    gateway: Gateway

    def __init__(self, gateway: Gateway) -> None:
        super().__init__()
        self.gateway = gateway

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        # create request from environment
        LOG.debug(
            "[%s] %s %s%s",
            threading.current_thread().name,
            environ["REQUEST_METHOD"],
            environ.get("HTTP_HOST"),
            environ["RAW_URI"],
        )
        request = Request(environ)
        if "asgi.headers" in environ:
            # restores raw headers from ASGI scope, which allows dashes in header keys
            # see https://github.com/pallets/werkzeug/issues/940
            request.headers = Headers(environ["asgi.headers"].raw_items())
        else:
            # by default, werkzeug requests from environ are immutable
            request.headers = Headers(request.headers)

        # prepare response
        response = Response()

        self.gateway.process(request, response)

        return response(environ, start_response)
