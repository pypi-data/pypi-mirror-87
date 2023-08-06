from os import path

from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import settings as _settings


class Leofile(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255, unique=True)
    content = models.TextField(verbose_name=_('content'), blank=True, default='')

    class Meta:
        verbose_name = _('leofile')
        verbose_name_plural = _('leofiles')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def content_type(self):
        _, ext = path.splitext(self.name)
        ext = ext.lstrip('.')
        return _settings.EXTENSION_CONTENT_TYPE_MAP.get(ext)
