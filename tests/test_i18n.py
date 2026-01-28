from fast_zero.i18n import init_gettext, translate_openapi_schema


def test_init_gettext_returns_translator_for_pt():
    g = init_gettext('pt')
    assert callable(g)
    # known translation in locales/pt
    assert g('Get greeting') == 'Obter saudação'
    # untranslated string should return itself (fallback True)
    assert g('This string is not translated') == (
        'This string is not translated'
    )


def test_init_gettext_uses_env_if_locale_none(monkeypatch):
    monkeypatch.setenv('APP_LOCALE', 'pt')
    g = init_gettext(None)
    assert g('Get greeting') == 'Obter saudação'


def test_translate_openapi_schema_translates_fields():
    g = init_gettext('pt')
    schema = {
        'info': {
            'title': 'Fast Zero API',
            'description': 'Returns a simple greeting message.',
        },
        'paths': {
            '/': {
                'get': {
                    'summary': 'Get greeting',
                    'description': 'Returns a simple greeting message.',
                }
            }
        },
        'components': {
            'schemas': {
                'Greeting': {
                    'description': 'Returns an HTML page with a greeting'
                }
            }
        },
    }

    out = translate_openapi_schema(schema, gettext_fn=g)
    assert out is schema
    assert out['info']['title'] == 'API Fast Zero'
    assert out['info']['description'] == (
        'Retorna uma mensagem de saudação simples.'
    )
    assert out['paths']['/']['get']['summary'] == 'Obter saudação'
    assert out['paths']['/']['get']['description'] == (
        'Retorna uma mensagem de saudação simples.'
    )
    assert out['components']['schemas']['Greeting']['description'] == (
        'Retorna uma página HTML com uma saudação'
    )


def test_translate_openapi_schema_handles_empty_and_non_dicts():
    assert translate_openapi_schema({}) == {}
    assert translate_openapi_schema(None) is None

    # paths entry that's not a dict should be skipped without error
    schema = {'paths': {'/': ['not', 'a', 'dict']}}
    out = translate_openapi_schema(schema, gettext_fn=init_gettext('pt'))
    assert out is schema
