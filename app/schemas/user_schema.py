from pydantic import BaseModel
from pydantic.types import UUID4


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserOutSchema(BaseModel):
    id: UUID4
    username: str
    email: str
