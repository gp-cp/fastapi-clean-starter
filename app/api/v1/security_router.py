import uuid
from typing import Annotated

import redis.asyncio as redis

from fastapi import APIRouter, Form, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse

from app.api.dependencies import get_user_service, get_store
from app.exceptions.user_exceptions import UserNotFound
from app.models.user_model import UserModel
from app.services.user_service import UserService

security_router = APIRouter(tags=["security"])


@security_router.post("/login", response_model=UserModel)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
    store: redis.Redis = Depends(get_store),
):
    try:
        user = await user_service.find_user_by_email(email)
    except UserNotFound:
        raise HTTPException(status_code=403, detail="Username or password wrong.")

    if not user.check_password(password):
        raise HTTPException(status_code=403, detail="Username or password wrong.")

    # Create a session for the user
    session_id = str(uuid.uuid4())
    await store.set(session_id, str(user.id), ex=3600)

    content = {"message": f"Welcome back {user.email}"}
    response = JSONResponse(content=content)
    response.set_cookie(
        key="fastapi_session",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=True,
    )
    return response


@security_router.get("/logout")
async def logout(
    fastapi_session: Annotated[str | None, Cookie()] = None,
    store: redis.Redis = Depends(get_store),
):
    if not fastapi_session:
        return {"message": "No session cookie found"}
    await store.delete(fastapi_session)
    content = {"message": "Goodbye"}
    response = JSONResponse(content=content)
    response.delete_cookie("fastapi_session")
    return response


@security_router.get("/check-session")
async def check_session(
    fastapi_session: Annotated[str | None, Cookie()] = None,
    store: redis.Redis = Depends(get_store),
    user_service: UserService = Depends(get_user_service),
):
    if not fastapi_session:
        return {"message": "No session cookie found"}
    user_id = await store.get(fastapi_session)
    if not user_id:
        return {"message": "Session expired"}

    user = await user_service.find_user_by_id(uuid.UUID(user_id.decode("utf-8")))

    return {"message": f"Welcome back {user.email}"}
