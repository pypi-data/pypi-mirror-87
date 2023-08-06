
from django.template.loader import render_to_string
from django.http.response import HttpResponseBadRequest

from pagination import paginate

from basement import http
from basement.forms import get_clean_data
from basement.views._base_view import BaseView


class FilterView(BaseView):

    def __init__(
            self,
            search_iterator,
            items_template,
            form_class=None,
            per_page=20,
            http_method='GET',
            form_factory=None,
            response_class=http.JsonResponse,
            response_factory=None,
            **kwargs):

        self._http_method = http_method
        self._items_template = items_template
        self._per_page = per_page

        setattr(self, http_method.lower(), self._process_request)

        self._search_iterator = search_iterator

        self._form_class = form_class

        if form_factory is not None:
            self._form_factory = form_factory

        self._response_class = response_class

        if response_factory is not None:
            self._response_factory = response_factory

        super(FilterView, self).__init__(**kwargs)

    def _process_request(self, request, **url_kwargs):

        form = self._get_form(request, url_kwargs)

        if form is None:
            data = {}
        else:
            data=get_clean_data(form)

        try:
            iterator = self._search_iterator(request, url_kwargs, data)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        return self._get_response(request, iterator)

    def _get_response(self, request, iterator):
        return self._response_factory(
            request=request,
            iterator=iterator,
            response_class=self._response_class
        )

    def _response_factory(self, request, iterator, response_class, **kwargs):

        page = paginate(
            request,
            iterator,
            per_page=self._per_page)

        return response_class({
            'items': render_to_string(self._items_template, {
                'request': request,
                'page_obj': page
            }),
            'has_next': page.has_next(),
            'next_page_url': '{}?{}'.format(
                request.path, page.next_page_number().querystring)
        })

    def _get_form(self, request, url_kwargs):

        if self._form_class:
            return self._form_factory(
                request=request,
                form_class=self._form_class,
                data=http.get_request_data(request),
                url_kwargs=url_kwargs)

        return None

    def _form_factory(self, request, form_class, data, url_kwargs):
        return form_class(data=data)
