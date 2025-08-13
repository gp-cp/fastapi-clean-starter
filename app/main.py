from fastapi import FastAPI

from app.api.v1.user_router import user_router
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
