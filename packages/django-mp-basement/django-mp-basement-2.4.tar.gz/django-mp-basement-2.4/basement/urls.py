
from django.apps import apps
from django.urls import path, include
from django.conf import settings

from pydoc import locate
from basement import views


def get_urlpatterns(is_db_download_enabled=False):

    result = [
        path('raise-exception/', lambda request: 1/0)
    ]

    if is_db_download_enabled:
        result.append(
            path('db/download/', views.download_db, name='download-db'))

    if apps.is_installed('ckeditor_uploader'):
        result.append(path('ckeditor/', include('ckeditor_uploader.urls')))

    for app in settings.INSTALLED_APPS:
        located_urls = locate('{}.urls.app_urls'.format(app))

        if not located_urls:
            continue

        result += located_urls

    return result