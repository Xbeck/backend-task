from datetime import date, datetime, time
from typing import List, Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from fastapi_cache.decorator import cache

from src.users.auth.dependencies import get_current_user
from src.users.models import UserOrm
from src.stadiums.dao import StadiumDAO
from src.stadiums.schemas import StadiumDTO
from src.stadiums.bookings.dao import BookingDAO
from src.users.schemas import UserDTO
from src.success_msgs import success_messages
from src.exceptions import (
    BadRequestException,
    BookingAlreadyExistsException,
    StadiumNotFoundException
)



router = APIRouter(
    prefix="/users",
    tags=["User endpoints"]
)


# 3.User
#     -Maydonlar ro'yhatini ko'rish.

#         Bunda ma'lum vaqt bilan filter qilish imkoni bo'lishi kerak,
#         yani kiritilgan vaqt oralig'idagi bron qilinmagan maydonlar ko'rsatiladi..

#         Turgan lokatsiyasi bo'yicha eng yaqin maydonlarni chiqarish bo'yicha sort ham bo'lishi kerak.
#         Hammasi bitta endpointda bo'ladi.
#     -Maydon haqida to'liq malumotni ko'rish
#     -Maydonni bron qilish


@router.get("/stadiums", status_code=200)
# @cache(expire=30)
async def get_all_stadiums(
    address: Literal["Marjonbuloq", "Bagarni", "Moltop", "G'allaorol shahar", "G'allaorol"] = None,
    selected_date: date = Query(..., description=f"Namuna: {datetime.now().date()}"),
    hour_from: Optional[int] = Query(None, description=f"Namuna: 10"),
    hour_to: Optional[int] = Query(None, description=f"Namuna: 12"),
    latitude: Optional[float] = Query(None, description=f"Namuna: 39.934467"), # Kenglik
    longitude: Optional[float] = Query(None, description=f"Namuna: 67.424750"), # Uzunlik
) -> List[StadiumDTO]:

    # if selected_date < date.today():
    #     raise BadRequestException

    current_location = None
    if latitude:
        current_location = (latitude, longitude)

    result = await StadiumDAO.find_all(
        address=address,
        select_date=selected_date,
        hour_from=hour_from,
        hour_to=hour_to,
        location=current_location
    )
    return result


@router.get("/stadiums/{stadium_id}", status_code=200)
# @cache(expire=30)
async def get_stadium(stadium_id: int) -> StadiumDTO:
    stadium = await StadiumDAO.find_one_or_none(id=stadium_id)
    if not stadium:
        raise StadiumNotFoundException
    return stadium


@router.post("/stadium/booking/add", status_code=201)
async def add_booking(stadium_id: int,
                      date: date,
                      hour_from: int,
                      hour_to: int,
                      background_tasks: BackgroundTasks,
                      current_user: UserOrm = Depends(get_current_user)
                      ):
    hour_from = time(hour_from, 0)
    hour_to = time(hour_to, 0)

    stadium = await StadiumDAO.find_one_or_none(id=stadium_id)
    if not stadium:
        raise StadiumNotFoundException

    booking = await BookingDAO.find_one_or_none(
        stadium_id=stadium_id,
        date=date,
        hour_from=hour_from,
        hour_to=hour_to)
    
    if booking:
        raise BookingAlreadyExistsException
    
    await BookingDAO.add(
        user_id=current_user.id,
        stadium_id=stadium_id,
        date=date,
        hour_from=hour_from,
        hour_to=hour_to,
    )
    return await success_messages("Stadium is booked")


@router.get("/me", status_code=200)
async def get_me(current_user: UserOrm = Depends(get_current_user)) -> UserDTO:
    return current_user
