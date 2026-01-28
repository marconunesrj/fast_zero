from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# O que cada linha da fixture faz?


# Resumindo, essa fixture está configurando e limpando um banco de dados de
# teste para cada teste que o solicita, assegurando que cada teste seja isolado
# e tenha seu próprio ambiente limpo para trabalhar.
# Isso é uma boa prática em testes de unidade, já que queremos que cada teste
# seja independente e não afete os demais.
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# Com essa fixture, sempre que precisarmos de um usuário em nossos testes,
# podemos simplesmente passar user como um argumento para nossos testes,
# e o Pytest se encarregará de criar um novo usuário para nós.
@pytest.fixture
def user(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    """
    Monkey patching é uma técnica em que modificamos ou estendemos o código em
    tempo de execução. Neste caso, estamos adicionando um novo atributo
    clean_password ao objeto user para armazenar a senha em texto puro.
    """
    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
