from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_zero.models import TodoState


class Message(BaseModel):
    message: str
    model_config = ConfigDict(
        schema_extra={'example': {'message': 'Usuário removido'}}
    )


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(
        schema_extra={
            'example': {
                'username': 'jdoe',
                'email': 'jdoe@example.com',
                'password': 'secret',
            }
        }
    )


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # Configuração para permitir a criação do modelo a partir de atributos de
    # uma classe como uma dataclass ou um modelo ORM
    model_config = ConfigDict(
        from_attributes=True,
        schema_extra={
            'example': {
                'id': 1,
                'username': 'jdoe',
                'email': 'jdoe@example.com',
            }
        },
    )


# class UserDB(UserSchema):
#     id: int


class UserList(BaseModel):
    users: list[UserPublic]
    model_config = ConfigDict(
        schema_extra={
            'example': {
                'users': [
                    {'id': 1, 'username': 'jdoe', 'email': 'jdoe@example.com'}
                ]
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str
    model_config = ConfigDict(
        from_attributes=True,
        schema_extra={
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                'eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.'
                'Nx0P_ornVwJBH_LLLVrlJoh6RmJeXR-Nr7YJ_mlGY04',
                'token_type': 'bearer',
            }
        },
    )


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, min_length=3, max_length=20)
    state: TodoState | None = None


# Todos os campos são opcionais para permitir atualizações parciais
class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
