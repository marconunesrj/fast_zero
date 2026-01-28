from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.i18n import init_gettext
from fast_zero.models import User
from fast_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

_ = init_gettext()

description_current_user = _('User ID')
description_skip = _('Number of items to skip')
description_limit = _('Max number of items to return')
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentId = Annotated[
    int, Path(..., description=description_current_user, example=1)
]
ItensSkip = Annotated[
    int,
    Query(description=description_skip),
]
ItensLimit = Annotated[
    int,
    Query(description=description_limit),
]

# Inicializa gettext (usa APP_LOCALE env ou 'pt' por padrão)
_ = init_gettext()

router = APIRouter(prefix='/users', tags=['users'])


# O "Depends" informa ao FastAPI que a função get_session deve ser chamada
# para fornecer o valor do parâmetro session. Isso permite que o FastAPI
# faça a injeção de dependências, facilitando o gerenciamento de recursos
# como sessões de banco de dados.
@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    summary=_('Create user'),
    description=_(
        'Creates a new user and returns the public user representation.'
    ),
    # tags=['Users'],
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
def create_user(user: UserSchema, session: Session):
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

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get(
    '/',
    response_model=UserList,
    summary=_('List users'),
    description=_('Returns a list of users (paginated).'),
    # tags=['Users'],
)
def read_users(session: Session, filter_users: Annotated[FilterPage, Query()]):
    """_('Returns a list of users (paginated).')"""
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    ).all()
    return {'users': users}


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    summary=_('Get user'),
    description=_('Return a single user by ID.'),
    # tags=['Users'],
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
    session: Session,
    user_id: CurrentId,
):
    """_('Return a single user by ID.')"""
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=_('User not found')
        )
    return db_user


@router.put(
    '/{user_id}',
    response_model=UserPublic,
    summary=_('Update user'),
    description=_('Update a user by ID and return the updated user.'),
    # tags=['Users'],
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
    session: Session,
    current_user: CurrentUser,
    user_id: CurrentId,
    user: UserSchema = None,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=_('Username or Email already exists'),
        )


@router.delete(
    '/{user_id}',
    response_model=Message,
    summary=_('Delete user'),
    description=_('Delete a user by ID and return a confirmation message.'),
    # tags=['Users'],
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
    session: Session,
    current_user: CurrentUser,
    user_id: CurrentId,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': _('User deleted')}
