
from django.http.response import HttpResponseBadRequest

from basement import http
from basement.forms import get_clean_data
from basement.views._base_view import BaseView


class FormActionView(BaseView):

    _message = None

    def __init__(
            self,
            action,
            form_class,
            http_method='POST',
            form_factory=None,
            response_class=http.JsonResponse,
            response_factory=None,
            message=None,
            **kwargs):

        self._http_method = http_method

        setattr(self, http_method.lower(), self._process_request)

        self._action = action

        self._form_class = form_class

        if form_factory is not None:
            self._form_factory = form_factory

        self._response_class = response_class

        if response_factory is not None:
            self._response_factory = response_factory

        if message is not None:
            self._message = message

        super(FormActionView, self).__init__(**kwargs)

    def _process_request(self, request, **url_kwargs):

        form = self._get_form(request, url_kwargs)

        try:
            action_result = self._action(
                request, url_kwargs,
                get_clean_data(form))
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

    def _get_form(self, request, url_kwargs):
        return self._form_factory(
            request=request,
            form_class=self._form_class,
            data=http.get_request_data(request),
            url_kwargs=url_kwargs)

    def _form_factory(self, request, form_class, data, url_kwargs):
        return form_class(data=data)
