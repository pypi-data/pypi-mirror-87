"""Test Authentication Lib"""
import pytest
from flask import Flask

from busie_flask.auth import AuthHelper, AuthError

@pytest.fixture
def mock_app(mocker):
    app = mocker.MagicMock()
    app.config.get.return_value = 'secret'
    return app

@pytest.fixture
def mock_oauth(mocker):
    return mocker.patch('busie_flask.auth.OAuth')

@pytest.fixture
def mock_app_with_client():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        AUTH0_ALGORITHMS='algorithms',
        AUTH0_AUDIENCE='audience',
        AUTH0_DOMAIN='domain',
        AUTH0_CLIENT_ID='id',
        AUTH0_CLIENT_SECRET='secret',
        AUTH0_BASE_URL='base',
        AUTH0_ACCESS_TOKEN_URL='access',
        AUTH0_AUTHORIZE_URL='authorize',
        AUTH0_JWKS_URI='jwks'
    )
    return app

def test_auth_error(mocker):
    """
    - Sets error, status_code to the provided values
    """
    mock_error = {'foo': 'bar'}
    mock_status_code = 401
    a = AuthError(mock_error, mock_status_code)
    assert isinstance(a, Exception)
    assert a.error == mock_error
    assert a.status_code == mock_status_code

    with pytest.raises(AuthError):
        raise AuthError(mock_error, mock_status_code)

def test_authentication_helper_init(mocker, mock_oauth):
    """
    - Sets __algorithms to None
    - Sets __domain to None
    - Sets __audience to None
    - Sets __client_secret to None
    - Sets __client_id to None
    - Sets __base_url to None
    - Sets __access_token_url to None
    - Sets __authorize_url to None
    - Sets __jwks_uri to None
    - Calls self.init_app with app if app provided
    """
    mock_init_app = mocker.patch('busie_flask.auth.AuthHelper.init_app')

    res = AuthHelper()
    mock_oauth.assert_called_once()
    mock_init_app.assert_not_called()
    properties = {
        ('__algorithms', None),
        ('__domain', None),
        ('__audience', None),
        ('__client_secret', None),
        ('__client_id', None),
        ('__base_url', None),
        ('__access_token_url', None),
        ('__authorize_url', None),
        ('__jwks_uri', None),
        ('__oauth', mock_oauth.return_value)
    }
    for prop, val in properties:
        assert hasattr(res, f'_AuthHelper{prop}'), f'AuthHelper does not have {prop} property'
        assert getattr(res, f'_AuthHelper{prop}') is val, f'AuthHelper.{prop} was not {val}'


    res = AuthHelper(app='foo')
    mock_init_app.assert_called_once_with('foo')


def test_init_app(mock_app, mocker, mock_oauth):
    """
    - Throws RuntimeError if app.config does not have AUTH_SECRET
    - Adds self to app.extensions as `auth`
    - registers auth0
    - adds /login route
    - adds /callback route
    - adds /logout route
    """
    del mock_app.extensions

    auth = AuthHelper()
    auth.init_app(mock_app)
    mock_oauth.return_value.init_app.assert_called_once_with(mock_app)
    mock_app.config.get.assert_has_calls([
        mocker.call('AUTH0_ALGORITHMS'),
        mocker.call('AUTH0_AUDIENCE'),
        mocker.call('AUTH0_DOMAIN'),
        mocker.call('AUTH0_CLIENT_SECRET'),
        mocker.call('AUTH0_CLIENT_ID'),
        mocker.call('AUTH0_BASE_URL'),
        mocker.call('AUTH0_ACCESS_TOKEN_URL'),
        mocker.call('AUTH0_AUTHORIZE_URL'),
        mocker.call('AUTH0_JWKS_URI')
    ], any_order=True)
    assert mock_app.extensions
    assert mock_app.extensions.get('auth') == auth
    assert auth._AuthHelper__algorithms == mock_app.config.get.return_value
    assert auth._AuthHelper__audience == mock_app.config.get.return_value
    assert auth._AuthHelper__domain == mock_app.config.get.return_value
    assert auth._AuthHelper__client_secret == mock_app.config.get.return_value
    assert auth._AuthHelper__client_id == mock_app.config.get.return_value
    assert auth._AuthHelper__base_url == mock_app.config.get.return_value
    assert auth._AuthHelper__access_token_url == mock_app.config.get.return_value
    assert auth._AuthHelper__authorize_url == mock_app.config.get.return_value
    assert auth._AuthHelper__jwks_uri == mock_app.config.get.return_value

    mock_oauth.return_value.register.assert_called_once_with('auth0',
        client_id=auth._AuthHelper__client_id, client_secret=auth._AuthHelper__client_secret,
        api_base_url=auth._AuthHelper__base_url, access_token_url=auth._AuthHelper__access_token_url,
        authorize_url=auth._AuthHelper__authorize_url, jwks_uri=auth._AuthHelper__jwks_uri,
        client_kwargs={'scope': 'openid profile email'}
    )
    mock_app.route.assert_has_calls([
        mocker.call('/login', methods=['GET']),
        mocker.call('/callback', methods=['GET']),
        mocker.call('/logout', methods=['GET'])
    ], any_order=True)

    mock_app.config.get.return_value = None
    with pytest.raises(RuntimeError):
        auth.init_app(mock_app)

def test_login_route(mock_app_with_client, mock_oauth, mocker):
    """
    - Invoke auth0.authorize_redirect with kw
    - return result
    """
    mock_url_for = mocker.patch('busie_flask.auth.url_for')
    auth = AuthHelper()
    auth.init_app(mock_app_with_client)
    mock_oauth.return_value.register.return_value.authorize_redirect.return_value = ('ok', 200)
    with mock_app_with_client.test_client() as c:
        c.get('/login')
        mock_url_for.assert_called_once_with('callback')
        mock_oauth.return_value.register.return_value.authorize_redirect.assert_called_once_with(
            redirect_uri=mock_url_for.return_value
        )

def test_logout_route(mocker, mock_oauth, mock_app_with_client):
    """
    - Clears the session
    - returns a redirect
    """
    mock_redirect = mocker.patch('busie_flask.auth.redirect')
    mock_redirect.return_value = ('ok', 200)
    mock_url_for = mocker.patch('busie_flask.auth.url_for')
    mock_session = mocker.patch('busie_flask.auth.session')
    mock_url_encode = mocker.patch('busie_flask.auth.urlencode')
    mock_url_encode.return_value = 'somestring'
    auth = AuthHelper()
    auth.init_app(mock_app_with_client)
    with mock_app_with_client.test_client() as c:
        c.get('/logout')
        mock_session.clear.assert_called_once()
        mock_url_for.assert_called_once_with('login', _external=True)
        mock_url_encode.assert_called_once_with({
            'returnTo': mock_url_for.return_value,
            'client_id': auth._AuthHelper__client_id
        })
        mock_redirect.assert_called_once()

def test_callback_route(mocker, mock_oauth, mock_app_with_client):
    """
    - Authorizes access token
    - Sets session data
    - redirects to '/'
    """
    mock_redirect = mocker.patch('busie_flask.auth.redirect')
    mock_redirect.return_value = ('ok', 200)
    mock_session = mocker.patch('busie_flask.auth.session', new=dict())
    auth = AuthHelper()
    auth.init_app(mock_app_with_client)
    with mock_app_with_client.test_client() as c:
        c.get('/callback')
        mock_oauth.return_value.register.return_value.authorize_access_token.assert_called_once()
        mock_oauth.return_value.register.return_value.get.assert_called_once_with('userinfo')
        mock_oauth.return_value.register.return_value.get.return_value.json.assert_called_once()
        mock_redirect.assert_called_once_with('/')
        assert 'jwt_payload' in mock_session
        assert 'profile' in mock_session




def test_get_token_auth_header(mocker):
    """
    - raise AuthError if `Authorization` not in request headers
    - raise AuthError if auth header does not have correct format
    - returns the token from the auth header
    """
    mock_request = mocker.patch('busie_flask.auth.request')
    valid_header = 'Bearer sometokenheredoesntmatter'
    invalid_headers = [
        None,
        'a token',
        'bearer',
        'some token with too many parts'
    ]
    auth = AuthHelper()
    for header in invalid_headers:
        mock_request.headers.get.return_value = header
        with pytest.raises(AuthError):
            auth.get_token_auth_header()
    mock_request.headers.get.return_value = valid_header
    token = auth.get_token_auth_header()
    assert isinstance(token, str)
    assert token == valid_header.split()[1]

def test_get_rsa_key_from_unverified_token(mocker):
    """
    - Raise AuthError if the provided token cannot be decoded as a jwt
    - Return an object representation of an RSA key if a match is found
    - Return None if a match is not found
    """
    mock_url_open = mocker.patch('busie_flask.auth.urlopen')
    mock_json = mocker.patch('busie_flask.auth.json')
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_jwt.JWTError = Exception
    mock_domain = 'foobar.com'
    mock_token = 'sometokendoesntmatteraslongasitsastring'
    mock_jwk = {'kid': 'someKID', 'kty': 'someKTY', 'use': 'someUSE', 'n': 'n', 'e': 'e'}
    mock_json.loads.return_value = {
        'keys': [mock_jwk]
    }
    mock_jwt.get_unverified_header.return_value = {'kid': mock_jwk['kid']}

    auth = AuthHelper()
    auth._AuthHelper__domain = mock_domain
    rsa_key = auth.get_rsa_key_from_unverified_token(mock_token)
    
    mock_url_open.assert_called_once_with(
        f'https://{mock_domain}/.well-known/jwks.json'
    )
    mock_json.loads.assert_called_once_with(mock_url_open.return_value.read.return_value)
    mock_jwt.get_unverified_header.assert_called_once_with(mock_token)
    assert rsa_key is not None
    assert 'kty' in rsa_key and rsa_key['kty'] == mock_jwk['kty']
    assert 'kid' in rsa_key and rsa_key['kid'] == mock_jwk['kid']
    assert 'use' in rsa_key and rsa_key['use'] == mock_jwk['use']
    assert 'n' in rsa_key and rsa_key['n'] == mock_jwk['n']
    assert 'e' in rsa_key and rsa_key['e'] == mock_jwk['e']

    mock_jwt.get_unverified_header.return_value = {'kid': 'invalid'}
    assert auth.get_rsa_key_from_unverified_token(mock_token) is None

    mock_jwt.get_unverified_header.side_effect = mock_jwt.JWTError
    with pytest.raises(AuthError):
        auth.get_rsa_key_from_unverified_token(mock_token)

def test_handle_rsa_decode(mocker):
    """
    - Raise AuthError on token expired
    - Raise AuthError on InvalidClaimsError
    - return the decoded token object
    """
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    class MockExpiredSignature(Exception):
        """Mock Expired Signature Error"""
    class MockInvalidClaims(Exception):
        """Mock Invalid Claims Error"""

    mock_token = 'sometoken'
    mock_key = {'alg': 'RS256', 'use': 'sig', 'n': 'thenvalue', 'e': 'theevalue'}
    mock_algorithms = ['algos']
    mock_domain = 'foo.com'
    mock_audience = 'someaudience'
    auth = AuthHelper()
    auth._AuthHelper__domain = mock_domain
    auth._AuthHelper__algorithms = mock_algorithms
    auth._AuthHelper__audience = mock_audience

    decoded = auth.handle_rsa_decode(mock_key, mock_token)
    mock_jwt.decode.assert_called_once_with(
        mock_token,
        mock_key,
        algorithms=mock_algorithms,
        audience=mock_audience,
        issuer=f'https://{mock_domain}/'
    )
    assert decoded == mock_jwt.decode.return_value

    mock_jwt.ExpiredSignatureError = MockExpiredSignature
    mock_jwt.JWTClaimsError = MockInvalidClaims
    exceptions = [mock_jwt.ExpiredSignatureError, mock_jwt.JWTClaimsError, AuthError]
    for e in exceptions:
        mock_jwt.decode.side_effect = e
        args_list = [
            mock_key if e is not AuthError else {},
            'token'
        ]
        with pytest.raises(AuthError):
            auth.handle_rsa_decode(*args_list)

def test_requires_web_auth(mocker):
    """
    - Redirects to the login page if profile is not in the session
    - Invokes the decorated function if the user is authorized
    """
    was_called = mocker.MagicMock()
    mock_session = mocker.patch('busie_flask.auth.session', new=dict())
    mock_redirect = mocker.patch('busie_flask.auth.redirect')
    mock_url_for = mocker.patch('busie_flask.auth.url_for')

    auth = AuthHelper()
    
    @auth.requires_web_auth
    def foo(*args, **kwargs):
        return was_called(*args, **kwargs)

    res = foo('something', **{'something': 'else'})
    was_called.assert_not_called()
    mock_url_for.assert_called_once_with('login')
    mock_redirect.assert_called_once_with(mock_url_for.return_value)

    mock_session['profile'] = {'foo': 'bar'}
    res = foo('something', **{'something': 'else'})
    was_called.assert_called_once_with('something', **{'something': 'else'})
    assert res == was_called.return_value



def test_requires_api_auth(mocker):
    """
    - Raise an auth error if AuthError is caught
    - Raise an auth error if base Exception is caught
    - Raise an auth error if get rsa key returns None
    - invokes the decorated function after setting request context current user
    """
    was_called = mocker.MagicMock()
    mock_get_auth_header = mocker.patch('busie_flask.auth.AuthHelper.get_token_auth_header')
    mock_get_rsa_key = mocker.patch('busie_flask.auth.AuthHelper.get_rsa_key_from_unverified_token')
    mock_handle_decode = mocker.patch('busie_flask.auth.AuthHelper.handle_rsa_decode')
    mock_context = mocker.patch('busie_flask.auth._request_ctx_stack')
    auth = AuthHelper()

    @auth.requires_api_auth
    def foo(*args, **kwargs):
        return was_called(*args, **kwargs)

    res = foo('something', **{'something': 'else'})
    was_called.assert_called_once_with('something', **{'something': 'else'})
    assert res == was_called.return_value
    mock_get_auth_header.assert_called_once()
    mock_get_rsa_key.assert_called_once_with(mock_get_auth_header.return_value)
    mock_handle_decode.assert_called_once_with(mock_get_rsa_key.return_value, mock_get_auth_header.return_value)
    assert mock_context.top.current_user == mock_handle_decode.return_value

    mock_get_rsa_key.return_value = None
    with pytest.raises(AuthError):
        foo()

    mock_get_auth_header.side_effect = AuthError
    with pytest.raises(AuthError):
        foo()

    mock_get_auth_header.side_effect = Exception
    with pytest.raises(AuthError):
        foo()

def test_requires_scope(mocker):
    """
    - Return True if the required scope is in the token scopes
    - Return False otherwise
    """

    mock_token = 'sometoken'
    mock_get_token = mocker.patch('busie_flask.auth.AuthHelper.get_token_auth_header')
    mock_get_token.return_value = mock_token
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_jwt.get_unverified_claims.return_value = {'scope': 'foo bar foobar'}

    auth = AuthHelper()
    assert auth.requires_scope('foo')
    mock_get_token.assert_called_once()
    mock_jwt.get_unverified_claims.assert_called_once_with(mock_token)

    assert not auth.requires_scope('somethingnotthere')
    mock_jwt.get_unverified_claims.return_value = {}
    assert not auth.requires_scope('foo')

def test_requires_permission(mocker):
    """
    - Return True if the permission is in the list of token permissions
    - Return False otherwise
    """
    mock_token = 'sometokenstring'
    mock_get_token = mocker.patch('busie_flask.auth.AuthHelper.get_token_auth_header')
    mock_get_token.return_value = mock_token
    mock_jwt = mocker.patch('busie_flask.auth.jwt')
    mock_unverified_claims = {'permissions': ['some:perm', 'someother:perm']}
    mock_jwt.get_unverified_claims.return_value = mock_unverified_claims

    auth = AuthHelper()
    assert auth.requires_permission(mock_unverified_claims['permissions'][0])
    mock_get_token.assert_called_once()
    mock_jwt.get_unverified_claims.assert_called_once_with(mock_token)
    
    assert not auth.requires_permission('something:invalid')
    mock_jwt.get_unverified_claims.return_value = {}
    assert not auth.requires_permission(mock_unverified_claims['permissions'][0])