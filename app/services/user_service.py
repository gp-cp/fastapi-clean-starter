from pydantic.types import UUID4

from app.exceptions.user_exceptions import UserNotFound, UserAlreadyExists
from app.models.user_model import UserModel
from app.repositories.user_repo import UserRepo
from app.schemas.user_schema import UserCreateSchema


class UserService:
    def __init__(self, db):
        self.user_repo = UserRepo(db)

    async def find_user_by_id(self, user_id: UUID4) -> UserModel:
        result = await self.user_repo.get_by_id(user_id)
        if not result:
            raise UserNotFound(user_id)
        return UserModel(**result)

    async def create_user(self, user_schema: UserCreateSchema) -> UserModel:
        # Check if the user exists.
        user = await self.user_repo.get_by_email(user_schema.email.lower())
        if user:
            raise UserAlreadyExists(user_schema.email)

        user = UserModel(
            email=user_schema.email.lower(), **user_schema.model_dump(exclude={"email"})
        )
        await self.user_repo.create(user.model_dump(by_alias=True))
        return user
