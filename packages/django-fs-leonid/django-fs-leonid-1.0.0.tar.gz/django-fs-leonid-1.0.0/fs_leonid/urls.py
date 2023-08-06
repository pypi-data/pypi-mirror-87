from django.urls import re_path

from . import settings as _settings
from .views import leofile_view


urlpatterns = [
    re_path(
        r'^(?P<name>\w+\.(?:{0}))$'.format(r'|'.join(_settings.EXTENSION_CONTENT_TYPE_MAP.keys())),
        leofile_view, name='leofile'
    ),
]
