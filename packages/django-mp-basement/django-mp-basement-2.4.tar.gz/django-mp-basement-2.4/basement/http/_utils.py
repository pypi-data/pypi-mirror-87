
from django.http import QueryDict


def get_request_body_querydict(request):

    if request.environ.get('CONTENT_TYPE', '').startswith('multipart'):
        raise ValueError("Multipart content type is not supported.")
    else:
        return QueryDict(request.body, encoding=request.encoding)


def get_request_data(request):
    if request.method in ('PUT', 'DELETE'):
        return get_request_body_querydict(request)
    return getattr(request, request.method)
