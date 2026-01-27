from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.i18n import init_gettext
from fast_zero.schemas import UserPublic

_ = init_gettext()


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': _('Olá Mundo!')}  # Assert


def test_root_deve_retornar_ok_e_ola_mundo_html(client: TestClient):

    response = client.get('/html')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    expected_html = """
        <html>
            <head>
                <title> {} </title>
            </head>
            <body>
                <h1> {} </h1>
            </body>
        </html>""".format(_('Nosso olá mundo!'), _('Olá Mundo'))

    assert response.text == expected_html


def test_create_user(client: TestClient):

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_error_username_exist(client: TestClient, user):

    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': _('Username already exists')}


def test_create_user_error_email_exist(client: TestClient, user):

    response = client.post(
        '/users/',
        json={
            'username': 'Aline',
            'email': 'teste@test.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': _('Email already exists')}


# client é uma fixture definida em tests/conftest.py
def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


# client é uma fixture definida em tests/conftest.py
# user é uma fixture definida em tests/conftest.py
def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


# client é uma fixture definida em tests/conftest.py
# user é uma fixture definida em tests/conftest.py
def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')
    assert response.json() == user_schema


# client é uma fixture definida em tests/conftest.py
# user é uma fixture definida em tests/conftest.py
def test_read_user_not_found(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': _('User not found')}


def test_update_user_error_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': _('User not found')}


# Quando usamos a fixture user, um usuário já é criado no banco de dados
# de teste antes do teste ser executado.
def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': _('Username or Email already exists')
    }


# Quando usamos a fixture user, um usuário já é criado no banco de dados
# de teste antes do teste ser executado.
def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': _('User deleted')}


def test_delete_user_error_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': _('User not found')}
