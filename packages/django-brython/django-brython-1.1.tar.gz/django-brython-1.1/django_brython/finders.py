import functools
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from . import consts


class BaseFinder:
    def find(self, path):
        """
        Given a relative file path, find an absolute file path.
        """
        raise NotImplementedError('subclasses of BaseFinder must provide a find() method')


class AppDirectoriesFinder(BaseFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The list of apps that are handled
        self.dirs = []
        # Mapping of app names to storage instances
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            self.dirs.append(Path(app_config.path))

    def find(self, path: str):
        tested = []

        module, relative_path = path.split('/', 1)
        for dir_ in self.dirs:
            full_path = dir_ / relative_path
            if dir_.name == module:
                if full_path.is_file():
                    return full_path, tested

            tested.append(full_path)

        return None, tested


def find(path):
    for finder in get_finders():
        result = finder.find(path)
        if result:
            return result


def get_finders():
    for finder_path in getattr(settings, 'BRYTHONFILES_FINDERS', consts.BRYTHONFILES_FINDERS):
        yield get_finder(finder_path)


@functools.lru_cache(maxsize=None)
def get_finder(import_path):
    Finder = import_string(import_path)
    if not issubclass(Finder, BaseFinder):
        raise ImproperlyConfigured('Finder "%s" is not a subclass of "%s"' %
                                   (Finder, BaseFinder))
    return Finder()
