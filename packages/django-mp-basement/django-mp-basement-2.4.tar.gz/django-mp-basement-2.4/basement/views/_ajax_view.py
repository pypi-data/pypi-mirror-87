
from functools import wraps

from basement import http
from basement.views._view import View


def ajax_view(http_method='GET', **kwargs):
    def decorator(f):
        return wraps(f)(
            View(
                f,
                http_method,
                response_class=http.JsonResponse,
                **kwargs
            )
        )
    return decorator
