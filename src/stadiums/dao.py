import logging
from datetime import time, date
from math import radians, sin, cos, sqrt, atan2

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, select

from src.database import async_session_maker
from src.base import BaseDAO
from src.stadiums.models import StadiumOrm
from src.stadiums.bookings.models import BookingOrm



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Yer radiusi, km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


class StadiumDAO(BaseDAO):
    model = StadiumOrm


    @classmethod
    async def find_all(cls,
                       address: str = None,
                       select_date: int = None,
                       hour_from: int = None,
                       hour_to: int = None,
                       location: tuple = None
                       ):
        """
        -- date = '14-12-2024'
        -- hour_from = '10:00'
        -- hour_to = '12:00'

        SELECT b.stadium_id
        FROM bookings b
        WHERE(
            ON b.stadium_id = stadiums.id
            AND b.date = date
            AND (
                (b.hour_from < '12:00' AND b.hour_to > '10:00')
            )
        )
        """
        try:
            async with async_session_maker() as session:
                # 3-urinish:
                # filter_date = date(2024, 12, select_date)
                hour_from = time(hour_from, 0)
                hour_to = time(hour_to, 0)

                subquery = (
                    select(BookingOrm.stadium_id)
                    .where(
                        BookingOrm.stadium_id == StadiumOrm.id,
                        BookingOrm.date == select_date,
                        and_(BookingOrm.hour_from < hour_to, BookingOrm.hour_to > hour_from),
                    )
                )

                """
                SELECT *
                FROM stadiums
                WHERE (
                    id NOT IN subquery AND address LIKE '%Marjonbuloq%'
                )
                """
                available_stadiums = select(StadiumOrm).filter(
                    ~StadiumOrm.id.in_(subquery), # stadion_id bor bo'lsa uni chiqarmaydi(hisobga olmaslik)
                    # StadiumOrm.id.in_(subquery) # hisobga oladi
                    StadiumOrm.address.like(f"%{address}%")
                )

                result = await session.execute(available_stadiums)
                result_orm = result.scalars().all()
                print(f"{result_orm=}")

                # Masofani hisoblash va saralash
                user_lat = location[0]
                user_lon = location[1]

                stadiums_with_distance = [
                    {
                        **jsonable_encoder(stadium),
                        "distance": haversine(user_lat, user_lon, stadium.latitude, stadium.longitude)
                    }
                    for stadium in result_orm
                ]

                sorted_stadiums = sorted(stadiums_with_distance, key=lambda x: x["distance"])
                for stadium in sorted_stadiums:
                    print(f"{stadium['name']} - {stadium['distance']:.2f} km")
                return sorted_stadiums

        except Exception as e:
            logging.error(e)
            raise


    @classmethod
    async def is_booked(cls,
                        stadium_id: int,
                        select_date: int = None,
                        hour_from: int = None,
                        hour_to: int = None):

        """
        -- date = '14-12-2024'
        -- hour_from = '12:00'
        -- hour_to = '13:00'

        """
        try:
            async with async_session_maker() as session:
                # 2-urinish:
                filter_date = date(2024, 12, select_date)
                hour_from = time(hour_from, 0)
                hour_to = time(hour_to, 0)
                subquery = (
                    select(BookingOrm.stadium_id)
                    .where(
                        BookingOrm.stadium_id == stadium_id,
                        BookingOrm.date == filter_date,
                        and_(BookingOrm.hour_from < hour_to, BookingOrm.hour_to > hour_from),
                    )
                )
                result = await session.execute(subquery)
                result_orm = result.scalars().first()
                print(f"{result_orm=}")

                if result_orm:
                    return True
                return False

        except Exception as e:
            logging.error(e)
            raise