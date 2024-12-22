from typing import List, Optional

from pydantic import BaseModel, ConfigDict

# from src.stadiums.bookings.schemas import BookingDTO



class StadiumAddDTO(BaseModel):
    name: str
    address: str
    contact: str
    images: List[int]
    price_per_hour: int
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_id: int
        
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "id": 1
            }
        }
    )


class StadiumDTO(StadiumAddDTO):
    id: int
    distance: Optional[float]


class StadiumRelDTO(StadiumDTO):
    bookings: List["BookingDTO"]


class StadiumUpdateDTO(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    images: Optional[List[int]] = None
    price_per_hour: Optional[int] = None
    description: Optional[str] = None
