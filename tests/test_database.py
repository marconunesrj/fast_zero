from types import SimpleNamespace

import pytest

from fast_zero import database


# Testa se o gerador get_session fecha a sessão ao sair do contexto
def test_get_session_generator_closes_on_exit(monkeypatch):
    # Criando uma classe de contexto de sessão falsa para simular o
    # comportamento da sessão do SQLAlchemy
    class DummySessionCtx:
        def __init__(self, engine):
            self._obj = SimpleNamespace(closed=False)

        def __enter__(self):
            return self._obj

        def __exit__(self, exc_type, exc, tb):
            self._obj.closed = True

    # Função de fábrica que retorna a classe de contexto de sessão falsa
    def dummy_session_factory(engine):
        return DummySessionCtx(engine)

    # Usando monkeypatch para substituir a função Session do módulo database
    monkeypatch.setattr(database, 'Session', dummy_session_factory)

    # Testando o gerador get_session
    gen = database.get_session()
    # Obtendo a primeira sessão do gerador
    session = next(gen)
    assert hasattr(session, 'closed')
    assert session.closed is False

    # Finalizando o gerador, o que deve fechar a sessão
    with pytest.raises(StopIteration):
        next(gen)

    # Verificando se a sessão foi fechada
    assert session.closed is True
