from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Leofile


def leofile_view(request, name):
    leofile = get_object_or_404(Leofile, name=name)
    content = leofile.content
    content_type = leofile.content_type
    return HttpResponse(content=content, content_type=content_type)
