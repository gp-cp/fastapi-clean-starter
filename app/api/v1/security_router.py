from fastapi import APIRouter, Form, Depends, HTTPException

from app.api.dependencies import get_user_service
from app.exceptions.user_exceptions import UserNotFound
from app.models.user_model import UserModel
from app.services.user_service import UserService

security_router = APIRouter(tags=["security"])


@security_router.post("/login", response_model=UserModel)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.find_user_by_email(email)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.check_password(password):
        raise HTTPException(status_code=404, detail="Incorrect password")
