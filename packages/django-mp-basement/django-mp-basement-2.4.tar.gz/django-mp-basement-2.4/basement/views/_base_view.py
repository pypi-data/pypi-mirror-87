
from basement import http
from basement.utils import decorate
from basement.views._request_dispatcher import RequestDispatcher


class BaseView(object):

    def __init__(self, decorators=None):
        self._decorators = decorators

    def __add__(self, other):
        return RequestDispatcher([self]) + other

    def __call__(self, request, *args, **kwargs):

        handler = getattr(
            self, request.method.lower(),
            self._handle_unsupported_method)

        handler = decorate(handler, self._decorators)

        return handler(request, *args, **kwargs)

    def _handle_unsupported_method(self, *args, **kwargs):
        raise http.UnsupportedMethod()
