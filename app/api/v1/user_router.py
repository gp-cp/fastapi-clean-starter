from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from app.api.dependencies import get_user_service
from app.exceptions.user_exceptions import UserNotFound, UserAlreadyExists
from app.schemas.user_schema import UserOutSchema, UserCreateSchema

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/{user_id}", response_model=UserOutSchema, description="Get a single user by id."
)
async def get_one(user_id: UUID, user_service=Depends(get_user_service)):
    try:
        user = await user_service.find_user_by_id(user_id=user_id)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {e} not found."
        )
    return user


@user_router.post(
    "/create", response_model=UserOutSchema, description="Create a new user."
)
async def create(user: UserCreateSchema, user_service=Depends(get_user_service)):
    try:
        user = await user_service.create_user(user_schema=user)
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {e} already exists.",
        )
    return user
