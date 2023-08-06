
from django.http.response import HttpResponseBadRequest

from basement import http
from basement.views._base_view import BaseView


class ActionView(BaseView):

    _message = None

    def __init__(
            self,
            action,
            http_method='POST',
            response_class=http.JsonResponse,
            response_factory=None,
            message=None,
            **kwargs
            ):

        self._http_method = http_method

        setattr(self, http_method.lower(), self._process_request)

        self._action = action

        self._response_class = response_class

        if response_factory is not None:
            self._response_factory = response_factory

        if message is not None:
            self._message = message

        super(ActionView, self).__init__(**kwargs)

    def _process_request(self, request, **url_kwargs):

        try:
            action_result = self._action(
                request, url_kwargs, http.get_request_data(request))
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        return self._get_response(request, action_result)

    def _get_response(self, request, action_result):
        return self._response_factory(
            request=request,
            action_result=action_result,
            message=self._message,
            response_class=self._response_class
        )

    def _response_factory(self, **kwargs):
        result = (kwargs.get('action_result') or {}).copy()
        result['message'] = kwargs['message']
        return kwargs['response_class'](result)
