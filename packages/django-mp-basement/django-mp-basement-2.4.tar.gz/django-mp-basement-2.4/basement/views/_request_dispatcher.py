
from basement import http


class RequestDispatcher(object):

    def __init__(self, views):
        self._views = views

    def __iter__(self):
        for view in self._views:
            yield view

    def __add__(self, other):

        try:
            other_views = list(other)
        except TypeError:
            other_views = [other]

        return RequestDispatcher(self._views + other_views)

    def __call__(self, request, *args, **kwargs):
        for view in self._views:
            try:
                return view(request, *args, **kwargs)
            except http.UnsupportedMethod:
                pass

        raise http.UnsupportedMethod()