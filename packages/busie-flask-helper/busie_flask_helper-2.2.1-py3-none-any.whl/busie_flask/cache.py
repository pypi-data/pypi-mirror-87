"""Cache Client Lib"""
from redis import Redis


class CacheClient:
    """
    Implements a redis client with flask based config

    Only public methods are set and get methods at this time, as it is all that is needed
    """

    def __init__(self, app=None):
        self.__redis = None

        if app is not None:
            self.init_app(app)

    @property
    def redis(self):
        """Return the redis instance"""
        return self.__redis

    def init_app(self, app):
        """
        Initialize a flask application with the cache client, and add it to the
        application's extensions
        """
        HOST = app.config.get('REDIS_HOST')
        PORT = app.config.get('REDIS_PORT')
        PASSWORD = app.config.get('REDIS_PASSWORD')
        DB = app.config.get('REDIS_DB')
        if not (HOST and PORT and isinstance(DB, int)):
            raise RuntimeError(
                'A valid `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` and `REDIS_DB` must be'
                ' provided to app config'
            )
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['CacheClient'] = self
        self.__redis = Redis(host=HOST, port=PORT, password=PASSWORD, db=DB)

    def set(self, name=None, value=None, ex=None):
        """
        Set in cache.
        """
        return self.__redis.set(name, value, ex=ex)

    def get(self, *args, **kwargs):
        """
        Retrieve from cache.
        """
        return self.__redis.get(*args, **kwargs)