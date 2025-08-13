from pydantic import BaseModel, Field
from pydantic.types import UUID4


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserSchema(BaseModel):
    id: UUID4
    username: str
    email: str
