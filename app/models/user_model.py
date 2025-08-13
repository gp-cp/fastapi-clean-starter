from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic.types import UUID4


class UserModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4, alias="_id")
    username: str
    email: str
    password: str
