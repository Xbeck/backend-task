from datetime import datetime, time

from pydantic import BaseModel

from src.users.schemas import UserDTO
from src.stadiums.schemas import StadiumDTO


class BookingAddDTO(BaseModel):
    date: datetime
    hour_from: time
    hour_to: time
    # price: int
    # total_cost: int
    # total_hours: int
    user_id: int
    stadium_id: int


class BookingDTO(BookingAddDTO):
    id: int


class BookingRelDTO(BookingDTO):
    user: "UserDTO"
    stadium: "StadiumDTO"
