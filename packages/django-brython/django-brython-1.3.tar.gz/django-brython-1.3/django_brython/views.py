import posixpath

from importlib import import_module
from pathlib import Path

from django.conf import settings

from django.http import Http404
from django.views import static


def serve(request, path, **kwargs):
    if not settings.DEBUG:
        raise Http404

    module_path = posixpath.normpath(path).lstrip('/').replace('.py', '').replace('/', '.')

    try:
        module = import_module(module_path)
    except ModuleNotFoundError:
        raise Http404(f"'import {module_path}' exception, file: {path} can't be served")

    imported_module_path = Path(module.__file__)

    if not module.__file__.endswith(path):
        raise Http404(f"Requested and imported module doesn't match. Imported: {module.__file__}, requested: {path}")

    return static.serve(request, imported_module_path.name, document_root=imported_module_path.parent, **kwargs)
