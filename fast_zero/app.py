from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.i18n import init_gettext, translate_openapi_schema
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

# Inicializa gettext (usa APP_LOCALE env ou 'pt' por padrão)
_ = init_gettext()

app = FastAPI(
    title=_('Fast Zero API'),
    description=_('API de exemplo para o curso FastAPI'),
    version='0.2.0',
)


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


# O "Depends" informa ao FastAPI que a função get_session deve ser chamada
# para fornecer o valor do parâmetro session. Isso permite que o FastAPI
# faça a injeção de dependências, facilitando o gerenciamento de recursos
# como sessões de banco de dados.
@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    summary=_('Create user'),
    description=_(
        'Creates a new user and returns the public user representation.'
    ),
    tags=['Users'],
    responses={
        HTTPStatus.CONFLICT.value: {
            'description': _('Conflict'),
            'content': {
                'application/json': {
                    'example': {'detail': _('Username already exists')}
                }
            },
        }
    },
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    """_('Creates a new user and returns the public user representation.')"""
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=_('Username already exists'),
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=_('Email already exists'),
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/users/',
    response_model=UserList,
    summary=_('List users'),
    description=_('Returns a list of users (paginated).'),
    tags=['Users'],
)
def read_users(
    skip: int = Query(0, description=_('Number of items to skip'), example=0),
    limit: int = Query(
        100, description=_('Max number of items to return'), example=100
    ),
    session: Session = Depends(get_session),
):
    """_('Returns a list of users (paginated).')"""
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}',
    response_model=UserPublic,
    summary=_('Get user'),
    description=_('Return a single user by ID.'),
    tags=['Users'],
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'description': _('Not found'),
            'content': {
                'application/json': {
                    'example': {'detail': _('User not found')}
                }
            },
        }
    },
)
def read_user(
    user_id: int = Path(..., description=_('User ID'), example=1),
    session: Session = Depends(get_session),
):
    """_('Return a single user by ID.')"""
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=_('User not found')
        )
    return db_user


@app.put(
    '/users/{user_id}',
    response_model=UserPublic,
    summary=_('Update user'),
    description=_('Update a user by ID and return the updated user.'),
    tags=['Users'],
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'description': _('Not found'),
            'content': {
                'application/json': {
                    'example': {'detail': _('User not found')}
                }
            },
        },
        HTTPStatus.CONFLICT.value: {
            'description': _('Conflict'),
            'content': {
                'application/json': {
                    'example': {
                        'detail': _('Username or Email already exists')
                    }
                }
            },
        },
    },
)
def update_user(
    user_id: int = Path(..., description=_('User ID'), example=1),
    user: UserSchema = None,
    session: Session = Depends(get_session),
):
    """_('Update a user by ID and return the updated user.')"""

    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=_('User not found')
        )

    try:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=_('Username or Email already exists'),
        )


@app.delete(
    '/users/{user_id}',
    response_model=Message,
    summary=_('Delete user'),
    description=_('Delete a user by ID and return a confirmation message.'),
    tags=['Users'],
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'description': _('Not found'),
            'content': {
                'application/json': {
                    'example': {'detail': _('User not found')}
                }
            },
        },
        HTTPStatus.OK.value: {
            'description': _('Successful deletion'),
            'content': {
                'application/json': {'example': {'message': _('User deleted')}}
            },
        },
    },
)
def delete_user(
    user_id: int = Path(..., description=_('User ID'), example=1),
    session: Session = Depends(get_session),
):
    """_('Delete a user by ID and return a confirmation message.')"""
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=_('User not found')
        )

    session.delete(db_user)
    session.commit()

    return {'message': _('User deleted')}


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
