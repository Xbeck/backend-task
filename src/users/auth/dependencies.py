from datetime import datetime

from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy import select

from src.admin.dao import RoleDAO
from src.config import settings
from src.users.dao import UserDAO
from src.users.models import UserOrm



def get_token(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user



async def user_is_admin(user: UserOrm = Depends(get_current_user)):
    user_role = await RoleDAO.find_by_id(model_id=user.role_id)
    if user_role.role_name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user

async def user_is_landman(user: UserOrm = Depends(get_current_user)):
    user_role = await RoleDAO.find_by_id(model_id=user.role_id)
    if user_role.role_name != "landman":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


