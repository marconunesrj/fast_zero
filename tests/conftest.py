from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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


"""
Explicando linha a linha, o código abaixo faz o seguinte:

class UserFactory(factory.Factory): define uma fábrica para o modelo User,
herdando de factory.Factory.

class Meta: uma classe interna Meta é usada para configurar a fábrica.

model = User: define o modelo para o qual a fábrica está construindo
instâncias. No caso, estamos referenciando a classe User, que deve ser um
modelo de banco de dados, como o SQLAlchemy.

username = factory.Sequence(lambda n: f'test{n}'): define um campo username
que recebe uma sequência. A cada chamada da fábrica, o valor n é incrementado,
então cada instância gerada terá um username único. Usando a string 'test{n}'.

email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com'): define
o campo email gerado a partir do username.

password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com'):
define o campo password similar ao campo email.
"""


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


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
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
    # table_registry.metadata.create_all(engine)

    # with Session(engine) as session:
    #     yield session

    # table_registry.metadata.drop_all(engine)
    # engine.dispose()


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# Com essa fixture, sempre que precisarmos de um usuário em nossos testes,
# podemos simplesmente passar user como um argumento para nossos testes,
# e o Pytest se encarregará de criar um novo usuário para nós.
# Este usuário está sendo usada para representar o usuário que está autenticado
# através do token.
@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    """
    Monkey patching é uma técnica em que modificamos ou estendemos o código em
    tempo de execução. Neste caso, estamos adicionando um novo atributo
    clean_password ao objeto user para armazenar a senha em texto puro.
    """
    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
