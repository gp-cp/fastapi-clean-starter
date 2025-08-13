from fastapi import FastAPI

from app.api.v1 import v1_router
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(v1_router, prefix="/api")
