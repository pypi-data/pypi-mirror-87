
from django.contrib import admin
from django.shortcuts import render as django_render

from django.contrib.admin.views.decorators import staff_member_required

from basement.views import render_view
from basement.utils import decorate


@staff_member_required
def render(request, template_name, context=None, status=None):

    ctx = admin.site.each_context(request)
    ctx.update(context or {})

    return django_render(request, template_name, ctx, status=status)


def admin_render_view(*args, **kwargs):

    def decorator(f):
        return decorate(f, decorators=[
            staff_member_required,
            render_view(*args, **kwargs, renderer=render)
        ])

    return decorator
