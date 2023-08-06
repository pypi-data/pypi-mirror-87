
from django.utils.translation import ugettext_lazy as _


class _ExtendedHttpException(Exception):

    def __init__(self, content=None):
        self._content = content
        super(_ExtendedHttpException, self).__init__()

    def __unicode__(self):
        message = 'HTTP error'
        if type(self._content) is dict and self._content.get('message'):
            message = self._content.get('message')
        return message

    def get_content(self):
        return self._content


class UnsupportedMethod(_ExtendedHttpException):

    def __init__(self):
        super(UnsupportedMethod, self).__init__(
            _("Selected http method is not supported."))
