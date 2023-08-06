"""Unit Test the cache Client"""
import pytest

from busie_flask.cache import CacheClient


def test_cache_init(mocker):
    """
    - sets _redis property to None
    - self.init_app if `app` is provided
    - does not init app if app not provided
    """
    mock_init_app = mocker.patch('busie_flask.cache.CacheClient.init_app')
    CacheClient()
    mock_init_app.assert_not_called()

    CacheClient(app='foo')
    mock_init_app.assert_called_once_with('foo')

def test_init_app(mock_redis, mocker):
    """
    - sets the extensions dictionary on the application if it does not exist
    - adds `cache` to the extensions
    - sets self._redis
    - raise runtime error if REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB not in app config
    """
    redis_mock = mock_redis('busie_flask.cache')
    cache = CacheClient()
    app = mocker.MagicMock()
    app.config.get.side_effect = lambda param: 0 if param == 'REDIS_DB' else 'foo'

    # Delete extensions from the mock to ensure that the dict is added in the event
    # That it does not already exist within the application instance
    del app.extensions

    cache.init_app(app)
    redis_mock.assert_called_once_with(
        host='foo',
        port='foo',
        password='foo',
        db=0
    )
    assert hasattr(app, 'extensions')
    assert 'CacheClient' in app.extensions
    assert cache.redis

    with pytest.raises(AttributeError):
        cache.redis = 'i shouldnt be able to do this'

    app_configs = [
        dict(REDIS_HOST='foo', REDIS_PASSWORD='BAR', REDIS_DB='foobar'),
        dict(REDIS_HOST='foo', REDIS_PASSWORD='BAR', REDIS_PORT='foobar'),
        dict(REDIS_PORT='foo', REDIS_DB='BAR', REDIS_PASSWORD='foobar')
    ]

    for conf in app_configs:
        app.config = conf
        with pytest.raises(RuntimeError):
            cache.init_app(app)


def test_set(mocker):
    cache = CacheClient()
    cache._CacheClient__redis = mocker.MagicMock()
    cache.set('foo', 'bar')
    cache._CacheClient__redis.set.assert_called_once_with('foo', 'bar', ex=None)

def test_get(mocker):
    cache = CacheClient()
    cache._CacheClient__redis = mocker.MagicMock()
    cache.get('foo')
    cache._CacheClient__redis.get.assert_called_once_with('foo')