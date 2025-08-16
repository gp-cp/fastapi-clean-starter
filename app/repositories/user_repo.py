from uuid import UUID
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class UserRepo:
    def __init__(self, db: AsyncDatabase):
        self.db = db
        self.collection = db.get_collection("users")

    async def get_by_id(self, user_id: UUID):
        return await self.collection.find_one({"_id": user_id})

    async def get_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create(self, user) -> InsertOneResult:
        return await self.collection.insert_one(user)
