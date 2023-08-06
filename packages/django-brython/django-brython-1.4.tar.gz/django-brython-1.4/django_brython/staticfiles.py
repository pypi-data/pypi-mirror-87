import tempfile
from importlib import import_module

from brython import list_modules, make_package
from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from pathlib import Path

from django.core.files import File
from django.core.files.storage import Storage
from django.utils.module_loading import import_string


class TempDirStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = tempfile.TemporaryDirectory()

    def path(self, name):
        return f'{self.directory.name}/{name}'

    def _open(self, name, mode):
        name = name.split('/')[-1]  # Don't handle directory structure in tempdir
        return File(open(f'{self.directory.name}/{name}', mode))


class BrythonStaticGenerator(BaseFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        module_path = Path(__file__).parent

        fronted_app = getattr(settings, 'BRYTHON_MAIN_MODULE', None)
        if not fronted_app:
            raise NotImplementedError
        else:
            self.brython_module_path = Path(import_module(fronted_app).__file__).parent
            # fronted_app = import_string(fronted_app)

        self.storage = TempDirStorage()
        """stdlib_path = Path(apps.get_app_config('django_brython').path) / 'static/django_brython/js/brython_stdlib.js'
        brython_stdlib = list_modules.parse_stdlib(stdlib_dir=stdlib_path.parent, js_name='brython_stdlib.js')
        user_modules = list_modules.load_user_modules(module_dir=module_path)
        # print(user_modules)

        self.brython_user_module = brython_user_module



        # stdlib_dir, stdlib = list_modules.load_stdlib_sitepackages()

        path = Path.cwd() / 'frontend'

        # finder.make_brython_modules()
        #print(finder.modules)"""

    def list(self, ignore_patterns):
        files = []

        #user_modules = list_modules.load_user_modules(self.brython_module_path)
        #finder = list_modules.ModulesFinder(directory=str(self.brython_module_path), stdlib={}, user_modules=user_modules)
        #finder.inspect()
        # print(finder.modules)
        #finder.make_brython_modules(f'{self.storage.directory.name}/{self.brython_module_path.name}')

        make_package.make(package_name=self.brython_module_path.name,
                          package_path=str(self.brython_module_path),
                          output_path=f'{self.storage.directory.name}/{self.brython_module_path.name}.brython.js')

        files.append((f'{self.brython_module_path.name}/js/{self.brython_module_path.name}.brython.js', self.storage))

        return files
