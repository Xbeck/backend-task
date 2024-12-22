import json
import logging
from typing import Iterable
from datetime import datetime

from src.stadiums.bookings.dao import BookingDAO
from src.stadiums.dao import StadiumDAO
from src.users.dao import UserDAO
from src.admin.dao import RoleDAO
from src.users.auth.auth import get_password_hash


TABLE_MODEL_MAP = {
    "stadiums": StadiumDAO,
    "users": UserDAO,
    "bookings": BookingDAO,
    "role": RoleDAO
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, val in row.items():
                if val.isdigit() and k not in ["latitude", "longitude"]:
                    row[k] = int(val)
                elif k in ["latitude", "longitude"]:
                    row[k] = float(val)
                elif val and k in ["permissions", "images"]:
                    row[k] = json.loads(val.replace("'", '\''))
                elif k in ["date", "registred_at"]:
                    row[k] = datetime.strptime(val, '%d-%m-%Y')
                elif "hour" in k:
                    row[k] = datetime.strptime(val, '%H:%M')
                elif val and k == "hashed_password":
                    row[k] = get_password_hash(password=str(val))

            data.append(row)
        return data
    except Exception as e:
        logging.error(f"Cannot convert CSV into DB format --> {e}")
