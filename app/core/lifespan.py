import redis.asyncio as redis

from fastapi import FastAPI

from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager
from .logger import logger
from pymongo.errors import ConnectionFailure
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo_client = AsyncMongoClient(
        settings.MONGO_URI, tz_aware=True, uuidRepresentation="standard"
    )
    app.db = app.mongo_client.get_database(settings.MONGO_DB)
    try:
        await app.mongo_client.db.command("ping")
        logger.info("Connected to MongoDB")
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")

    app.redis_client = redis.Redis()

    try:
        await app.redis_client.ping()
        logger.info("Connected to Redis")
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")

    yield

    await app.mongo_client.close()
    await app.redis_client.aclose()
