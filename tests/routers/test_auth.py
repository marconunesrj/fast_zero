from http import HTTPStatus

from freezegun import freeze_time

from fast_zero.i18n import init_gettext
from fast_zero.models import User

_ = init_gettext()


def test_get_token(client, user):
    """
    Monkey patching é uma técnica em que modificamos ou estendemos o código em
    tempo de execução. Neste caso, O atributo clean_password foi criado na
    @pytest.fixture no objeto user para armazenar a senha em texto puro.
    """
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_error_not_user(client):
    user = User(
        username='NoOne',
        email='noone@example.com',
        password='secreterro',
    )
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_error_verify_password(client, user):
    """
    Monkey patching é uma técnica em que modificamos ou estendemos o código em
    tempo de execução. Neste caso, O atributo clean_password foi criado na
    @pytest.fixture no objeto user para armazenar a senha em texto puro.
    """
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password + 'erro',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


"""
criaremos nosso teste. Começaremos pegando um token para um usuário,
congelando o tempo, esperando pelo tempo de expiração do token e,
em seguida, tentando usar o token para acessar um endpoint que requer
autenticação.

Ao elaborarmos o teste, usaremos a funcionalidade de congelamento
de tempo do freezegun. O objetivo é simular a criação de um
token às 12:00 e, em seguida, verificar sua expiração às 12:31.
Neste cenário, estamos utilizando o conceito de "viajar no tempo"
para além do período de validade do token, garantindo que a tentativa
subsequente de utilizá-lo resultará em um erro de autenticação.
"""


def test_token_expired_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
