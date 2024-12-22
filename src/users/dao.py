from src.base import BaseDAO
from src.users.models import UserOrm

class UserDAO(BaseDAO):
    model = UserOrm