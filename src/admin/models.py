from sqlalchemy import JSON, Column, Integer, String

from src.database import Base


class RoleOrm(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False) # admin, landman, user
    permissions = Column(JSON, nullable=False)

 # {"create": True, "read": True, "update": True, "delete": True}