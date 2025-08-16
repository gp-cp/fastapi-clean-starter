from http.client import HTTPException
from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

PH = PasswordHasher()


class UserModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4, alias="_id")
    username: str
    email: str
    password: str

    def hash_password(self) -> str:
        self.password = PH.hash(self.password)

    def check_password(self, password: str) -> bool:
        try:
            PH.verify(self.password, password)
        except VerifyMismatchError:
            return False
        except InvalidHashError:
            return False
        return True
