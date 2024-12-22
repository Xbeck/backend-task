from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base




class UserOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    registred_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.id"))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship
    stadiums = relationship("StadiumOrm", back_populates="user")
    bookings = relationship("BookingOrm", back_populates="user")

    def __str__(self) -> str:
        return f"User {self.email}"



# 3.User
#     -Maydonlar ro'yhatini ko'rish.
#       Bunda ma'lum vaqt bilan filter qilish imkoni bo'lishi kerak,
#       yani kiritilgan vaqt oralig'idagi bron qilinmagan maydonlar ko'rsatiladi.
#       Turgan lokatsiyasi bo'yicha eng yaqin maydonlarni chiqarish bo'yicha sort ham bo'lishi kerak.
#       Hammasi bitta endpointda bo'ladi.

#     -Maydon haqida to'liq malumotni ko'rish
#     -Maydonni bron qilish