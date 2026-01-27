from pydantic import BaseModel, ConfigDict, EmailStr


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
