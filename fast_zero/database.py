# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_zero.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


"""
expire_on_commit=False, estamos dizendo ao SQLAlchemy para não expirar
os objetos carregados após um commit, o que é importante
no contexto assíncrono.
O comportamento padrão do SQLAlchemy é expirar o cache de objetos
após um commit, o que pode causar problemas em operações assíncronas,
pois o objeto pode ser descartado enquanto estamos aguardando em outra
corrotina. Por isso, usamos expire_on_commit=False para evitar esse
tipo de comportamento.
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
"""


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# engine = create_engine(Settings().DATABASE_URL)


# def get_session():
#     with Session(engine) as session:
#         # O yield permite que a função seja usada como um gerador
#         # de contexto, fornecendo uma sessão de banco de dados
#         # para operações dentro do bloco "with".
#         # Após o bloco "with", a sessão é automaticamente fechada,
#         # garantindo o gerenciamento adequado dos recursos.
#         # O yield pausa a execução da função, retornando o valor
#         # da sessão para o contexto chamador.
#         yield session
