"""
For loading in modules related to the application
"""

from os import walk
from os.path import abspath, basename, dirname, join
from importlib import import_module
from inspect import isclass
from sys import modules

from flask_sqlalchemy import Model
from flask.views import MethodView

class Loader:
    def __init__(self, root_dir=None):
        self._SRC_DIR = src_dir = abspath(root_dir)
        self._APP_MODULE = basename(src_dir)

    def get_modules(self, module):
        """
        Return all .py modules in a given module directory
        that are not __init__

        Usage:
            get_modules('models')

        Yields dot-notaed module paths for discovery/import
        i.e. src/app/models/foo.py > app.models.foo
        """

        file_dir = abspath(join(self._SRC_DIR, module))
        for root, _, files in walk(file_dir):
            mod_path = f"{self._APP_MODULE}{root.split(self._SRC_DIR)[1]}".replace('/', '.')
            for filename in files:
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    yield '.'.join([mod_path, filename[0:-3]])

    def dynamic_loader(self, module, compare):
        """
        Iterates over all .py files in `module` directory,
        finding all classes that match `compare` function.
        Other objects in the module directory are ignored.

        :return: unique list of matches
        """

        items = []
        for mod in self.get_modules(module):
            module = import_module(mod)
            if hasattr(module, '__all__'):
                objs = [getattr(module, obj) for obj in module.__all__]
                items += [o for o in objs if compare(o) and o not in items]
        return items

    def get_models(self, models_dir):
        """Dynamic Model Finder"""
        return self.dynamic_loader(models_dir, self.is_model)

    def is_model(self, item):
        """Determine if the `item` is a SQLAlchemy `Model` subclass"""
        return isclass(item) and issubclass(item, Model) and not item.__ignore__()

    def get_views(self, views_dir):
        """Dynamic View Finder"""
        return self.dynamic_loader(views_dir, self.is_view)

    def is_view(self, item):
        return isclass(item) and issubclass(item, MethodView) and not item.__ignore__()
    
    
    def load_models(self, models_dir):
        """Load application models from models_dir"""
        for model in self.get_models(models_dir):
            setattr(modules[__name__], model.__name__, model)