from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # Configuração para permitir a criação do modelo a partir de atributos de
    # uma classe como uma dataclass ou um modelo ORM
    model_config = ConfigDict(from_attributes=True)


# class UserDB(UserSchema):
#     id: int


class UserList(BaseModel):
    users: list[UserPublic]
