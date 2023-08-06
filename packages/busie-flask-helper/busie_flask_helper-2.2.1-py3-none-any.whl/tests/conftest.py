import pytest
from os.path import join, dirname, abspath

@pytest.fixture
def root_dir():
    return join(dirname(abspath(__file__)), '../')

@pytest.fixture
def async_mock(mocker):
    return lambda mod: lambda loc, **kwargs: mocker.patch(f"{loc}.{mod}", **kwargs)

@pytest.fixture
def mock_sql_alchemy(async_mock):
    return async_mock('SQLAlchemy')

@pytest.fixture
def mock_flask(async_mock):
    return async_mock('Flask')

@pytest.fixture
def mock_migrate(async_mock):
    return async_mock('Migrate')

@pytest.fixture
def mock_loader(async_mock):
    return async_mock('Loader')

@pytest.fixture
def mock_auth(async_mock):
    return async_mock('AuthHelper')

@pytest.fixture
def mock_cache(async_mock):
    return async_mock('CacheClient')

@pytest.fixture
def mock_force_auto_coercion(async_mock):
    return async_mock('force_auto_coercion')

@pytest.fixture
def mock_jwt(async_mock):
    return async_mock('jwt')

@pytest.fixture
def mock_redis(async_mock):
    return async_mock('Redis')
