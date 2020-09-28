import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):

    #send GET request to get registration page
    assert client.get('/auth/register').status_code == 200

    #send request to register a new user
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )

    #check the new user is registered and the page is redirected
    assert 'http://localhost/auth/login' == response.headers['Location']


    with app.app_context():
        #check new user was added to the database
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'User test is already registered.'),
))


def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data



def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
