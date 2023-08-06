from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import force_auto_coercion

from .loaders import Loader
from .auth import AuthHelper
from .cache import CacheClient


class FlaskHelper:
    """
    Helper class that abstracts database and view implementation
    by exposing helpful custom methods for ease of use in
    the Flask Application Factory pattern
    """
    def __init__(self, root_dir, app=None, models_dir=None, views_dir=None):
        self.__loader = Loader(root_dir=root_dir)
        self.__db = SQLAlchemy()
        self.__migrate = Migrate()
        self.__auth = AuthHelper()
        self.__cache = CacheClient()

        if app is not None and models_dir is not None and views_dir is not None:
            self.init_app(app, models_dir, views_dir)
    
    @property
    def db(self):
        """
        READONLY
        accesses the __db attribute
        """
        return self.__db

    @property
    def auth(self):
        """
        READONLY
        access the __auth attribute
        """
        return self.__auth

    @property
    def cache(self):
        """
        READONLY
        access the __cache attribute
        """
        return self.__cache

    def init_app(self, app, models_dir, views_dir):
        self._init_db(app=app, models_dir=models_dir)
        self._init_migrations(app=app)
        self._init_views(app=app, views_dir=views_dir)
        self._init_auth(app=app)
        self._init_cache(app=app)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['FlaskHelper'] = self

    def _init_db(self, app=None, models_dir=None):
        """Initialize the database object used by the application"""
        if isinstance(app, Flask):
            force_auto_coercion()
            self.__loader.load_models(models_dir)
            self.__db.init_app(app)
        else:
            raise ValueError('Cannot init DB without a valid Flask application')

    def _init_migrations(self, app=None):
        """Initialize the Migrate command"""
        if isinstance(app, Flask):
            self.__migrate.init_app(app, self.__db)
        else:
            raise ValueError('Cannot init Migrate command without a valid Flask application')

    def _init_auth(self, app=None):
        if isinstance(app, Flask):
            self.__auth.init_app(app)
        else:
            raise ValueError('Cannot init Authorization helper without a valid Flask application')

    def _init_cache(self, app=None):
        if isinstance(app, Flask):
            self.__cache.init_app(app)
        else:
            raise ValueError('Cannot init Cache Client without a valid Flask application')

    def _init_views(self, app=None, views_dir=None):
        """Initialize Application API Views"""
        if isinstance(app, Flask):
            for view in self.__loader.get_views(views_dir):
                try:
                    view_func = view.as_view(view.view_name())
                    for path, methods in view.get_url_rules():
                        app.add_url_rule(
                            path,
                            view_func=view_func,
                            methods=methods
                        )
                except AttributeError as exc:
                    print(
                        f"""
                        Could not add {view.__class__} to application url rules, 
                        as a required attribute was missing: {exc}
                        """
                    )
        else:
            raise ValueError('Cannot init application views without a valid Flask application')
