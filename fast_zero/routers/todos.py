from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


router = APIRouter(prefix='/todos', tags=['todos'])
"""
Neste código, criamos uma nova instância da classe APIRouter do FastAPI.
Esta classe é usada para definir as rotas de nossa aplicação.
A instância router funcionará como um mini aplicativo FastAPI,
que poderá ter suas próprias rotas, modelos de resposta, etc.

A opção prefix no construtor do APIRouter é usada para definir um prefixo
 comum para todas as rotas definidas neste roteador. Isso significa que
 todas as rotas que definirmos neste roteador começarão com /todos.
 Usamos um prefixo aqui porque queremos agrupar todas as rotas relacionadas
 a tarefas em um lugar. Isso torna nossa aplicação mais organizada e fácil
 de entender.

A opção tags é usada para agrupar as rotas em seções no documento interativo
 de API gerado pelo FastAPI (como Swagger UI e ReDoc). Todas as rotas que
 definirmos neste roteador aparecerão na seção "todos" da documentação da API.
"""


@router.get('/', response_model=TodoList)
async def list_todos(
    session: Session,
    # O parâmetro (current_user: CurrentUser) faz com que seja
    # requerida a autenticação
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    )

    return {'todos': todos.all()}


@router.post('/', response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema,
    # O parâmetro (current_user: CurrentUser) faz com que seja
    # requerida a autenticação
    user: CurrentUser,
    session: Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.patch('/{todo_id}', response_model=TodoPublic)
async def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    """
    A linha for key, value in todo.model_dump(exclude_unset=True).items():
    está iterando através de todos os campos definidos na instância todo
    do modelo de atualização. A função model_dump é um método que vem do
    modelo BaseModel do Pydantic e permite exportar o modelo para um
    dicionário.

    O parâmetro exclude_unset=True é importante aqui, pois significa que
    apenas os campos que foram explicitamente definidos (ou seja, aqueles
    que foram incluídos na solicitação PATCH) serão incluídos no dicionário
    resultante. Isso permite que você atualize apenas os campos que foram
    fornecidos na solicitação, deixando os outros inalterados.

    Após obter a chave e o valor de cada campo definido, a linha
    setattr(db_todo, key, value) é usada para atualizar o objeto db_todo que
    representa a tarefa no banco de dados. A função setattr é uma função
    embutida do Python que permite definir o valor de um atributo em um objeto.
    Neste caso, ele está definindo o atributo com o nome igual à chave
    (ou seja, o nome do campo) no objeto db_todo com o valor correspondente.

    Dessa forma, garantimos que somente os campos enviados ao schema sejam
    atualizados no objeto.
    """
    # Atualiza apenas os campos fornecidos no corpo da requisição
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
async def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    await session.delete(todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully.'}
