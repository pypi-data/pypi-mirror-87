import posixpath

from importlib.util import find_spec
from pathlib import Path

from django.conf import settings

from django.http import Http404
from django.views import static


def serve(request, path, **kwargs):
    if not settings.DEBUG:
        raise Http404

    module_path = posixpath.normpath(path).lstrip('/').replace('.py', '').replace('/', '.')

    module = find_spec(module_path)
    if not module:
        raise Http404(f"'import {module_path}' exception, file: {path} can't be served")

    tested_module_path = Path(module.origin)

    if not str(tested_module_path).endswith(path):
        raise Http404(f"Requested and imported module doesn't match. Imported: {module.origin}, requested: {path}")

    return static.serve(request, tested_module_path.name, document_root=tested_module_path.parent, **kwargs)
