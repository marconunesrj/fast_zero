import gettext
import os

_ = gettext.gettext


def init_gettext(locale: str | None = None):
    """Inicializa gettext para o `locale` informado e retorna `_()`.

    Procura por arquivos .mo em
    `fast_zero/locales/<locale>/LC_MESSAGES/messages.mo`.
    Retorna uma função `gettext` pronta para uso; não altera variáveis
    globais para evitar o uso de `global`.
    """

    if locale is None:
        locale = os.getenv('APP_LOCALE', 'pt')

    localedir = os.path.join(os.path.dirname(__file__), 'locales')

    translation = gettext.translation(
        'messages', localedir=localedir, languages=[locale], fallback=True
    )

    return translation.gettext


def translate_openapi_schema(schema: dict, gettext_fn=None) -> dict:
    """Traduz partes do schema OpenAPI (in-place) usando `gettext_fn`.

    Campos traduzidos:
    - info.title, info.description
    - paths[*].<method>.summary
    - paths[*].<method>.description
    - components.schemas[*].description
    """
    if not schema:
        return schema

    if gettext_fn is None:
        gettext_fn = _

    def _translate_if_present(obj, key):
        val = obj.get(key)
        if isinstance(val, str) and val:
            obj[key] = gettext_fn(val)

    info = schema.get('info')
    if isinstance(info, dict):
        _translate_if_present(info, 'title')
        _translate_if_present(info, 'description')

    paths = schema.get('paths', {})
    for methods in paths.values():
        if not isinstance(methods, dict):
            continue
        for op in methods.values():
            if not isinstance(op, dict):
                continue
            _translate_if_present(op, 'summary')
            _translate_if_present(op, 'description')

    components = schema.get('components', {}).get('schemas', {})
    for comp in components.values():
        if not isinstance(comp, dict):
            continue
        _translate_if_present(comp, 'description')

    return schema
