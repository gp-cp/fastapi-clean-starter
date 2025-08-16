import redis.asyncio as redis
from fastapi import Request, Depends
from pymongo.asynchronous.database import AsyncDatabase

from app.services.user_service import UserService


def get_db(request: Request) -> AsyncDatabase:
    return request.app.db


def get_store(request: Request) -> redis.Redis:
    return request.app.redis_client


def get_user_service(db=Depends(get_db)) -> UserService:
    return UserService(db)
