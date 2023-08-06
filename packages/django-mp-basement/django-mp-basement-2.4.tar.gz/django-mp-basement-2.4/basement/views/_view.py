
from django.http.response import HttpResponseBadRequest

from basement.views._base_view import BaseView


class View(BaseView):

    def __init__(
            self,
            action,
            http_method,
            response_class,
            decorators=None,
            errors_with_forms=False):

        self._action = action
        self._response_class = response_class
        self._errors_with_forms = errors_with_forms

        setattr(self, http_method.lower(), self._process_request)

        super(View, self).__init__(decorators=decorators)

    def _process_request(self, request, *args, **kwargs):

        try:
            action_result = self._action(request, *args, **kwargs)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        return self._response_class(action_result)
