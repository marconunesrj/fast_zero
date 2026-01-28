from http import HTTPStatus
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from fast_zero.app import login_for_access_token
from fast_zero.models import User
from fast_zero.security import get_password_hash

# Arquivo feito fora de padrão pelo Copilot


def test_login_for_access_token_success(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    form = SimpleNamespace(username=user.email, password=password)
    result = login_for_access_token(form_data=form, session=session)

    assert 'access_token' in result
    assert result['token_type'] == 'bearer'


def test_login_for_access_token_wrong_email(session):
    form = SimpleNamespace(username='noone@example.com', password='whatever')

    with pytest.raises(HTTPException) as excinfo:
        login_for_access_token(form_data=form, session=session)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED


def test_login_for_access_token_wrong_password(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    form = SimpleNamespace(username=user.email, password='badpassword')

    with pytest.raises(HTTPException) as excinfo:
        login_for_access_token(form_data=form, session=session)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
