from fastapi import APIRouter, Response

from src.users.auth.schemas import AuthDTO
from src.users.dao import UserDAO
from src.users.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.config import settings
from src.success_msgs import success_messages
from src.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth User"]
)


@router.post("/register", status_code=201)
async def register_user(user_data: AuthDTO):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)

    await UserDAO.add(email=user_data.email,
                       hashed_password=hashed_password,
                    #    role_id = 1
                       )
    return await success_messages("User registered", status_code=201)


@router.post("/login", status_code=200)
async def login_user(response: Response, user_data: AuthDTO):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise UserNotFoundException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(settings.COOKIE_NAME, access_token, httponly=True)
    return await success_messages("User registered", token=access_token)


@router.post("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie(settings.COOKIE_NAME)
    return await success_messages("User logged out")