from sqlalchemy import Column, Computed, Date, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship

from src.database import Base



class BookingOrm(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    stadium_id = Column(ForeignKey("stadiums.id"), nullable=False)
    date = Column(Date, nullable=False)
    hour_from = Column(Time, nullable=False)
    hour_to = Column(Time, nullable=False)

    # Relationship
    user = relationship("UserOrm", back_populates="bookings")
    stadium = relationship("StadiumOrm", back_populates="bookings")

    def __str__(self) -> str:
        return f"Booking #{self.id}"
    


    # price = Column(Integer, nullable=False)
    # hourplan_id = Column(ForeignKey("hourplan.id"), nullable=False)
    # # Преобразование разницы в количестве часов
    # total_hours = Column(Integer, Computed("EXTRACT(EPOCH FROM (hour_to - hour_from)) / 3600"))
    # # Использование total_hours для расчёта стоимости
    # total_cost = Column(Integer, Computed("(EXTRACT(EPOCH FROM (hour_to - hour_from)) / 3600) * price"))
