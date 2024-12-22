from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.users.auth.dependencies import user_is_landman
from src.stadiums.schemas import StadiumAddDTO, StadiumUpdateDTO
from src.stadiums.dao import StadiumDAO
from src.stadiums.bookings.dao import BookingDAO
from src.users.models import UserOrm
from src.success_msgs import success_messages
from src.exceptions import (
    StadiumAlreadyExistsException,
    StadiumNotFoundException,
)



router = APIRouter(
    prefix="/stadiums",
    tags=["Landman endpoints"]
)


# 2.Maydon egalari
#     -Futbol maydonni kiritish tahrirlash
#      (nomi, address, contact, rasmlari, 1soatlik bron qilish narxi, va hokazo). 
#     -Bronlarni ko'rish
#     -Bronni o'chirish

@router.post("/add", status_code=201)
async def add_stadium(stadium_data: StadiumAddDTO,
                      current_user: UserOrm = Depends(user_is_landman)):
    existing_stadium = await StadiumDAO.find_one_or_none(name=stadium_data.name)
    if existing_stadium:
        raise StadiumAlreadyExistsException
    await StadiumDAO.add(**stadium_data)
    return await success_messages("Stadium added")


@router.patch("/update", status_code=200)
async def update_stadium_data(new_data: StadiumUpdateDTO,
                              current_user: UserOrm = Depends(user_is_landman)):
    existing_stadium = await StadiumDAO.find_one_or_none(model_id=new_data.id)
    if not existing_stadium:
        raise StadiumNotFoundException
    await StadiumDAO.update(**new_data)
    return await success_messages("Data updated")


@router.get("/bookings/all", status_code=200)
# @cache(expire=30)
async def get_all_booking(
    current_user: UserOrm = Depends(user_is_landman)
):
    return await BookingDAO.find_all()


@router.get("/bookings/{booking_id}", status_code=204)
async def delete_booking(
    booking_id: int,
    current_user: UserOrm = Depends(user_is_landman)
):
    await BookingDAO.delete(model_id=booking_id)
    return await success_messages("Data deleted")


