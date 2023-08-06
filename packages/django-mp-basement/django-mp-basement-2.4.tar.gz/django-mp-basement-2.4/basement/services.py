
_SERVICES = {}


class ServiceLocator(object):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __getattr__(self, name):

        cached_name = '_cached_%s' % name

        try:
            return object.__getattribute__(self, cached_name)
        except AttributeError:
            service = self._resolve_service(name)
            setattr(self, cached_name, service)
            return service

    def _resolve_service(self, name):
        try:
            service_factory = _SERVICES[name]
        except KeyError:
            raise AttributeError(
                "Service '%s' is not available. "
                "Ensure this service is registred by @register_service "
                "decorator. Please note, in order for @register_service "
                "to be invoked at the project initialization stage it must "
                "be used inside the 'models' module of a django app." % name
            )

        return service_factory(self, **self._kwargs)


def register_service(name):
    def _decorator(service_factory):
        if name in _SERVICES:
            conflicting_service = _SERVICES[name]
            raise RuntimeError(
                "Cannot register a service under the name '%s'. "
                "This name is already taken by another service %s from %s." %
                (
                    name,
                    repr(conflicting_service),
                    conflicting_service.__module__
                )
            )
        _SERVICES[name] = service_factory
        return service_factory
    return _decorator
