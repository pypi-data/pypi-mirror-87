
from django.conf import settings

from basement.services import ServiceLocator


class RequestEnvironment(object):

    def __init__(self, session, user):

        self.session = session
        self.user = user
        self.is_debug = settings.DEBUG
        self._service_locator = ServiceLocator(user=user)

    def __getattr__(self, name):
        return getattr(self._service_locator, name)


class RequestEnvironmentMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session = getattr(request, 'session', None)
        request.env = RequestEnvironment(session, request.user)
        return self.get_response(request)
