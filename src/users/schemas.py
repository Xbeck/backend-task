from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr



class UserDTO(BaseModel):
    id: int
    email: EmailStr
    registred_at: datetime
    role_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "test@test.com",
                "registred_at": "15-11-2024",
                "role_id": 1
            }
        }
    )

class UserRelDTO(UserDTO):
    bookings: List["BookingDTO"]





