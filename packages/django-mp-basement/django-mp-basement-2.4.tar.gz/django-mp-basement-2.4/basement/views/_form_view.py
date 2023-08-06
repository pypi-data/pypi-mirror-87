
from basement import http
from basement.views._base_view import BaseView


class FormView(BaseView):

    def __init__(
            self,
            form_class,
            form_factory=None,
            response_class=http.JsonResponse,
            response_factory=None,
            **kwargs):

        self._form_class = form_class

        if form_factory is not None:
            self._form_factory = form_factory

        self._response_class = response_class

        if response_factory is not None:
            self._response_factory = response_factory

        super(FormView, self).__init__(**kwargs)

    def get(self, request, **url_kwargs):

        form = self._get_form(request, url_kwargs)

        return self._get_response(request, form)

    def _get_response(self, request, form):
        return self._response_factory(
            request=request,
            form=form,
            response_class=self._response_class
        )

    def _response_factory(self, **kwargs):
        return kwargs['response_class'](kwargs['form'])

    def _get_form(self, request, url_kwargs):

        if self._form_class is None:
            return None

        return self._form_factory(
            request=request,
            form_class=self._form_class,
            url_kwargs=url_kwargs)

    def _form_factory(self, **kwargs):
        return kwargs['form_class']()
