from sqladmin import ModelView

from src.admin.models import RoleOrm
from src.users.models import UserOrm
from src.stadiums.models import StadiumOrm
from src.stadiums.bookings.models import BookingOrm





class UserAdmin(ModelView, model=UserOrm):
    column_list = [UserOrm.id, UserOrm.email, UserOrm.role_id]
    column_details_exclude_list = [UserOrm.hashed_password]
    can_delete = False
    name = "Foydalanuvchi"
    name_plural = "Foydalanuvchilar"
    icon = "fa-solid fa-user"


class RoleAdmin(ModelView, model=RoleOrm):
    column_list = [RoleOrm.id, RoleOrm.permissions, RoleOrm.role_name]
    can_delete = False
    name = "Role"
    name_plural = "Roles"
    icon = "fa-solid fa-user-tag"


class StadiumAdmin(ModelView, model=StadiumOrm):
    column_list = [StadiumOrm.id, StadiumOrm.name, StadiumOrm.bookings]
    can_delete = False
    name = "Stadion"
    name_plural = "Stadionlar"
    icon = "fa-solid fa-graduation-cap"


class BookingsAdmin(ModelView, model=BookingOrm):
    column_list = [BookingOrm.id, BookingOrm.hour_from, BookingOrm.stadium_id, BookingOrm.user]
    can_delete = False
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-chart-line"