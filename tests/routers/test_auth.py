from http import HTTPStatus

from fast_zero.i18n import init_gettext

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
