from types import SimpleNamespace

import pytest

from fast_zero import database


# Testa se o gerador get_session fecha a sessão ao sair do contexto
@pytest.mark.asyncio
async def test_get_session_generator_closes_on_exit(monkeypatch):
    # Criando uma classe de contexto de sessão falsa para simular o
    # comportamento da sessão do SQLAlchemy (async context manager)
    class DummySessionCtx:
        def __init__(self, engine, **kwargs):
            self._obj = SimpleNamespace(closed=False)

        async def __aenter__(self):
            return self._obj

        async def __aexit__(self, exc_type, exc, tb):
            self._obj.closed = True

    # Função de fábrica que retorna a classe de contexto de sessão falsa
    def dummy_session_factory(engine, **kwargs):
        return DummySessionCtx(engine, **kwargs)

    # Usando monkeypatch para substituir AsyncSession no módulo database
    monkeypatch.setattr(database, 'AsyncSession', dummy_session_factory)

    # Testando o gerador get_session (é um async generator)
    gen = database.get_session()

    # Obtendo a primeira sessão do gerador (await em __anext__)
    session = await gen.__anext__()  # noqa: PLC2801
    assert hasattr(session, 'closed')
    assert session.closed is False

    # Finalizando o gerador, o que deve fechar a sessão
    await gen.aclose()

    # Verificando se a sessão foi fechada
    assert session.closed is True
