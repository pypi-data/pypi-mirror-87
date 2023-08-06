"""Test the Flask Helper Module"""
import pytest

from busie_flask import FlaskHelper

PACKAGE = 'busie_flask'

def test_init(mock_sql_alchemy, mock_migrate, mock_loader, mock_auth, mock_cache, mocker):
    """
    - Initialize a Loader instance with the provided root_dir
    - Initialize a SQLAlchemy instance
    - Initialize a Migrate instance
    - TODO: Initialize an Auth instance
    - init_app if app, models_dir, and views_dir provided
        NOTE typically these params will not be provided on initialization,
        as this helper class was built with the Application Factory pattern in mind
    """
    orm_mock = mock_sql_alchemy(PACKAGE)
    migrate_mock = mock_migrate(PACKAGE)
    loader_mock = mock_loader(PACKAGE)
    cache_mock = mock_cache(PACKAGE)
    auth_mock = mock_auth(PACKAGE)

    helper = FlaskHelper('/foo/bar')
    orm_mock.assert_called_once()
    migrate_mock.assert_called_once()
    loader_mock.assert_called_once_with(root_dir='/foo/bar')

    private_attributes = dict(
        _FlaskHelper__migrate=migrate_mock.return_value,
        _FlaskHelper__db=orm_mock.return_value,
        _FlaskHelper__auth=auth_mock.return_value,
        _FlaskHelper__loader=loader_mock.return_value,
        _FlaskHelper__cache=cache_mock.return_value
    )
    for attr, val in private_attributes.items():
        assert hasattr(helper, attr), f'Flask Helper instance has no `{attr}` attribute`'
        assert getattr(helper, attr) == val, f'Flask Helper instance `{attr}` was not `{val}`'

    # Test edge case usage
    mock_init_app = mocker.patch('busie_flask.FlaskHelper.init_app')
    FlaskHelper('/foo/bar', app='someapp', models_dir='somedir', views_dir='someotherdir')
    mock_init_app.assert_called_once_with('someapp', 'somedir', 'someotherdir')

@pytest.mark.parametrize(('read_only', 'private'), (
    ('db', '_FlaskHelper__db'),
    ('auth', '_FlaskHelper__auth'),
    ('cache', '_FlaskHelper__cache')
))
def test_readonly_properties(mock_sql_alchemy, mock_migrate, mock_loader, mock_auth, mock_cache, read_only, private):
    """
    - Read only property, (Raises when trying to set it)
    - returns desired private property
    """
    mock_sql_alchemy(PACKAGE)
    mock_migrate(PACKAGE)
    mock_loader(PACKAGE)
    mock_auth(PACKAGE)
    mock_cache(PACKAGE)

    h = FlaskHelper('/foo/bar')
    assert hasattr(h, read_only)
    assert getattr(h, read_only) == getattr(h, private)
    with pytest.raises(AttributeError):
        setattr(h, read_only, 'i shouldnt be able to do this')

def test_init_app(mock_migrate, mock_loader, mock_sql_alchemy, mocker):
    """
    - Initialize DB
    - Initailize migrations
    - Initialize Views
    - Initialize AuthHelper
    - Initialize CacheCLient
    - Adds FlaskHelper to app extensions
    """
    mock_loader(PACKAGE)
    mock_migrate(PACKAGE)
    mock_sql_alchemy(PACKAGE)
    app = mocker.MagicMock()
    del app.extensions
    models_dir = mocker.Mock()
    views_dir = mocker.Mock()
    mock_init_db = mocker.patch('busie_flask.FlaskHelper._init_db')
    mock_init_migrations = mocker.patch('busie_flask.FlaskHelper._init_migrations')
    mock_init_views = mocker.patch('busie_flask.FlaskHelper._init_views')
    mock_init_auth = mocker.patch('busie_flask.FlaskHelper._init_auth')
    mock_init_cache = mocker.patch('busie_flask.FlaskHelper._init_cache')

    helper = FlaskHelper('/foo/bar')
    helper.init_app(app, models_dir, views_dir)

    mock_init_db.assert_called_once_with(app=app, models_dir=models_dir)
    mock_init_migrations.assert_called_once_with(app=app)
    mock_init_views.assert_called_once_with(app=app, views_dir=views_dir)
    mock_init_auth.assert_called_once_with(app=app)
    mock_init_cache.assert_called_once_with(app=app)

    assert hasattr(app, 'extensions')
    assert app.extensions['FlaskHelper'] == helper

def test_init_db(mock_sql_alchemy, mock_migrate, mock_loader, mock_flask, mock_force_auto_coercion, mocker):
    """
    - Raises Value Error if provided app is not a Flask instance
    - force_auto_coercion()
    - loads models
    - db.init_app
    """
    class Flask(mocker.MagicMock):
        """mock the flask class"""
    mock_flask(PACKAGE, new=Flask)
    mock_migrate(PACKAGE)
    orm_mock = mock_sql_alchemy(PACKAGE)
    loader_mock = mock_loader(PACKAGE)
    force_auto_coercion_mock = mock_force_auto_coercion(PACKAGE)
    app = Flask()
    models_dir = mocker.Mock()

    helper = FlaskHelper('foo/bar')

    helper._init_db(app=app, models_dir=models_dir)
    force_auto_coercion_mock.assert_called_once()
    loader_mock.return_value.load_models.assert_called_once_with(models_dir)
    orm_mock.return_value.init_app.assert_called_once_with(app)

    with pytest.raises(ValueError):
        helper._init_db(app='invalid', models_dir='doesntmatter')

def test_init_migrations(mock_sql_alchemy, mock_migrate, mock_loader, mock_flask, mocker):
    """
    - Raise value error if app not valid Flask instance
    - migrate.init_app with app and sqlalchemy instance
    """
    class Flask(mocker.MagicMock):
        """mock the flask class"""
    mock_flask(PACKAGE, new=Flask)
    app = Flask()
    orm_mock = mock_sql_alchemy(PACKAGE)
    migrate_mock = mock_migrate(PACKAGE)
    mock_loader(PACKAGE)

    helper = FlaskHelper('foo/bar')
    helper._init_migrations(app=app)

    migrate_mock.return_value.init_app.assert_called_once_with(app, orm_mock.return_value)

    with pytest.raises(ValueError):
        helper._init_migrations(app='foo')

def test_init_auth(mock_flask, mock_loader, mock_sql_alchemy, mock_migrate, mock_auth, mock_cache, mocker):
    """
    - auth.init_app() with app
    - Raises ValueError if app provided is not a Flask instance
    """
    mock_migrate(PACKAGE)
    mock_sql_alchemy(PACKAGE)
    mock_loader(PACKAGE)
    auth_mock = mock_auth(PACKAGE)
    mock_cache(PACKAGE)

    class Flask(mocker.MagicMock):
        """mock the flask class"""
    mock_flask(PACKAGE, new=Flask)
    app = Flask()
    helper = FlaskHelper('foo')

    helper._init_auth(app=app)
    auth_mock.return_value.init_app.assert_called_once_with(app)

    with pytest.raises(ValueError):
        helper._init_auth(app='foobar')

def test_init_cache(mock_flask, mock_loader, mock_sql_alchemy, mock_migrate, mock_auth, mock_cache, mocker):
    """
    - cache.init_app() with app
    - Raises ValueError if app provided is not a Flask instance
    """
    mock_migrate(PACKAGE)
    mock_sql_alchemy(PACKAGE)
    mock_loader(PACKAGE)
    mock_auth(PACKAGE)
    cache_mock = mock_cache(PACKAGE)

    class Flask(mocker.MagicMock):
        """mock the flask class"""
    mock_flask(PACKAGE, new=Flask)
    app = Flask()
    helper = FlaskHelper('foo')

    helper._init_cache(app=app)
    cache_mock.return_value.init_app.assert_called_once_with(app)

    with pytest.raises(ValueError):
        helper._init_cache(app='foobar')


def test_init_views(mock_flask, mock_migrate, mock_sql_alchemy, mock_loader, mocker, capsys):
    """
    - Raises ValueError if provided app is not a valid Flask instance
    - loader.get_views
    - view.as_view(view.view_name()) for each view returned from get_views
    - view.get_url_rules for each view returned from get_views
    - app.add_url_rule for each rule returned from each view's get_url_rule
    """
    mock_migrate(PACKAGE)
    mock_sql_alchemy(PACKAGE)
    loader_mock = mock_loader(PACKAGE)
    class Flask(mocker.MagicMock):
        """mock the flask class"""
        add_url_rule = mocker.MagicMock()

    mock_flask(PACKAGE, new=Flask)
    app = Flask()
    views_dir = mocker.Mock()

    first_view = mocker.MagicMock()
    first_view.get_url_rules.return_value = (('foo', 'bar'),)
    second_view = mocker.MagicMock()
    second_view.get_url_rules.return_value = (('bar', 'foo'),)

    views = [first_view, second_view]

    loader_mock.return_value.get_views.return_value = views

    helper = FlaskHelper('foo/bar')
    helper._init_views(app=app, views_dir=views_dir)

    loader_mock.return_value.get_views.assert_called_once_with(views_dir)
    for view in views:
        view.view_name.assert_called_once()
        view.as_view.assert_called_once_with(view.view_name.return_value)
        view.get_url_rules.assert_called_once()

    app.add_url_rule.assert_has_calls(
        [
            mocker.call(
                first_view.get_url_rules.return_value[0][0],
                view_func=first_view.as_view.return_value,
                methods=first_view.get_url_rules.return_value[0][1]
            ),
            mocker.call(
                second_view.get_url_rules.return_value[0][0],
                view_func=second_view.as_view.return_value,
                methods=second_view.get_url_rules.return_value[0][1]
            )

        ]
    )

    with pytest.raises(ValueError):
        helper._init_views(app='foo')

    first_view.get_url_rules.side_effect = AttributeError
    helper._init_views(app=app)
    cap = capsys.readouterr()
    assert cap.out is not None
