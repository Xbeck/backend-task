from sqlalchemy import JSON, Column, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base




class StadiumOrm(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    images = Column(JSON, default=list)
    price_per_hour = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship
    user = relationship("UserOrm", back_populates="stadiums")
    bookings = relationship("BookingOrm", back_populates="stadium")

    def __str__(self) -> str:
        return f"Booking #{self.name}"


