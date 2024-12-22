from fastapi import Depends
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.config import settings





class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        # Установите ваш логин и пароль
        if username == "admin" and password == "admin":
            # access_token = create_access_token({"sub": str(user.id)})
            # request.session.update({"token": access_token})
            request.session.update({"user": username})
            return True
        return False


    async def logout(self, request: Request) -> bool:
        # Очистка сессии
        request.session.clear()
        return True

    # async def authenticate(self, request: Request) -> bool:
    #     token = request.session.get("token")

    #     if not token:
    #         return False
        
    #     user = await get_current_user(token)
    #     if not user or user.role_id != 4:  # Проверка роли администратора
    #         return False

    #     # Check the token in depth
    #     return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)   # Ваш секретный ключ