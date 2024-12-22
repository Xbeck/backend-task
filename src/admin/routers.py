from fastapi import APIRouter, Depends

from src.users.dao import UserDAO
from src.users.auth.dependencies import user_is_admin
from src.users.models import UserOrm


router = APIRouter(
    prefix="/admin",
    tags=["Admin endpoints"]
)

# Rollar va ular bajarishi mumkin bo'lgan amallar
# 1.Admin – barcha huquqlarga ega

@router.get("/users/all", status_code=200)
async def get_all_users(
    current_user: UserOrm = Depends(user_is_admin)
    ): # for Admin
    return await UserDAO.find_all()

@router.get("/users/{user_id}", status_code=200)
async def get_one_user(user_id: int,
                       current_user: UserOrm = Depends(user_is_admin)
                ):
    return await UserDAO.find_by_id(model_id=user_id)