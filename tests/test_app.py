from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.i18n import init_gettext

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
