
import re

from datetime import datetime

from django.conf import settings


def clean_code(text):
    return re.sub(r'[\W_]+', '', text).lower()


def get_date_from_request(request, key):
    return request.GET.get(
        key,
        datetime.now().date().strftime(settings.DATE_INPUT_FORMATS[0])
    )


def get_percent(i, total, max_val=100, decimals=1, ):
    return ("{0:." + str(decimals) + "f}").format(max_val * (i / float(total)))


def print_progress(
        i, total, prefix='Progress', decimals=1, length=100, fill='█'):

    percent = get_percent(i, total, decimals=decimals)

    filled = int(length * i // total)

    bar = fill * filled + '-' * (length - filled)

    print('\r{}: |{}| {}%'.format(prefix, bar, percent), end='\r')

    if i == total:
        print()


def decorate(f, decorators):

    if not decorators:
        return f

    decorated_f = f

    for decorator in reversed(decorators):
        decorated_f = decorator(decorated_f)

    return decorated_f
