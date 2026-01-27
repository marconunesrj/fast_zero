from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        # O yield permite que a função seja usada como um gerador
        # de contexto, fornecendo uma sessão de banco de dados
        # para operações dentro do bloco "with".
        # Após o bloco "with", a sessão é automaticamente fechada,
        # garantindo o gerenciamento adequado dos recursos.
        # O yield pausa a execução da função, retornando o valor
        # da sessão para o contexto chamador.
        yield session
