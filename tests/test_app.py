from http import HTTPStatus

from fastapi.testclient import TestClient

import fast_zero.app as app_mod
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


def test_openapi_translated_sets_and_returns_schema(monkeypatch):
    # import fast_zero.app as app_mod

    # Ensure no cached schema
    app_mod.app.openapi_schema = None

    # Stub original openapi to return a simple schema dict
    def fake_original_openapi():
        return {'info': {'title': 'fake'}}

    monkeypatch.setattr(app_mod, '_original_openapi', fake_original_openapi)

    called = {}

    # Fake translate that records args and mutates schema
    def fake_translate_openapi_schema(schema, gettext_fn=None):
        called['schema'] = schema
        called['gettext_fn'] = gettext_fn
        schema['translated'] = True

    monkeypatch.setattr(
        app_mod, 'translate_openapi_schema', fake_translate_openapi_schema
    )

    # Act
    result = app_mod.app.openapi()

    # Assert returned and cached schema, and translate was called
    # with correct args
    assert result == {'info': {'title': 'fake'}, 'translated': True}
    assert app_mod.app.openapi_schema is result
    assert called['schema'] is result
    assert called['gettext_fn'] is app_mod._


def test_openapi_translated_returns_cached_schema_if_present(monkeypatch):

    # Put a cached schema
    cached = {'cached': True}
    app_mod.app.openapi_schema = cached

    # Ensure translate_openapi_schema is not called
    def should_not_be_called(*a, **kw):
        raise AssertionError(
            'translate_openapi_schema should not '
            'be called when schema is cached'
        )

    monkeypatch.setattr(
        app_mod, 'translate_openapi_schema', should_not_be_called
    )

    # Act
    result = app_mod.app.openapi()

    # Assert the cached schema is returned unchanged
    assert result is cached
    assert result == {'cached': True}
