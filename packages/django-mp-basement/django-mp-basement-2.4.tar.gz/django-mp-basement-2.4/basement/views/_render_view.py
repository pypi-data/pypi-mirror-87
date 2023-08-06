
from django.shortcuts import render

from basement.utils import decorate


def render_view(template_name, renderer=render, decorators=None):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            context = decorate(view_func, decorators)(request, *args, **kwargs)

            return renderer(request, template_name, context)

        return wrapper

    return decorator
