import posixpath
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.views import static

from . import finders


def serve(request, path, **kwargs):
    if not settings.DEBUG:
        raise Http404

    path = posixpath.normpath(path).lstrip('/')

    if '/' not in path:
        raise Http404("relative import aren't allowed: {}".format(path))

    absolute_path, tested = finders.find(path)
    if not absolute_path:
        raise Http404("{} could not be found, tested paths: {}".format(
            str(path),
            ', '.join(str(_) for _ in tested)
        ))

    return static.serve(request, absolute_path.name, document_root=absolute_path.parent, **kwargs)

