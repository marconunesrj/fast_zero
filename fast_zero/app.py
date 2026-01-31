from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.i18n import init_gettext, translate_openapi_schema
from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

# Inicializa gettext (usa APP_LOCALE env ou 'pt' por padrão)
_ = init_gettext()

app = FastAPI(
    title=_('Fast Zero API'),
    description=_('API de exemplo para o curso FastAPI'),
    version='0.2.0',
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
    summary=_('Get greeting'),
    description=_('Returns a simple greeting message.'),
    tags=['General'],
)
def read_root():
    """_('Returns a simple greeting message.')"""
    return {'message': _('Olá Mundo!')}


# Retornando uma página HTML simples
@app.get(
    '/html',
    response_class=HTMLResponse,
    status_code=HTTPStatus.OK,
    summary=_('Get HTML greeting'),
    description=_('Returns an HTML page with a greeting'),
    tags=['General'],
)
def read_root_html():
    """_('Returns an HTML page with a greeting')"""
    return """
        <html>
            <head>
                <title> {} </title>
            </head>
            <body>
                <h1> {} </h1>
            </body>
        </html>""".format(_('Nosso olá mundo!'), _('Olá Mundo'))


# Sobrescreve o gerador OpenAPI para traduzir textos exibidos em docs.html
_original_openapi = app.openapi


def _openapi_translated():
    if app.openapi_schema:
        return app.openapi_schema

    schema = _original_openapi()
    translate_openapi_schema(schema, gettext_fn=_)
    app.openapi_schema = schema
    return schema


app.openapi = _openapi_translated
