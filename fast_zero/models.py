from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


"""
o conceito de relationship no SQLAlchemy. A função relationship
define como as duas tabelas irão interagir. Por exemplo, a tabela User,
em seu campo "todos" pode exibir todos os objetos Todo associados a ela.
Por exemplo, quando buscarmos por um User por meio de um select obteremos
todos N objetos Todo associados ao seu id:

Nesse caso temos uma relação de 1 User, para N Todo.

O argumento cascade determina o que ocorre com as tarefas quando o
usuário associado a elas é deletado. Ao definir 'all, delete-orphan',
estamos instruindo o SQLAlchemy a deletar todas as tarefas de um usuário
quando este for deletado.

O termo usado lazy='selectin' no relationship. Isso faz com que o novo campo
traga os resultados de Todos associados a esse User quando for
buscado via select.
"""


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


@mapped_as_dataclass(table_registry)
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
