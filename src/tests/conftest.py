import json
from datetime import datetime

import asyncio
import pytest
from sqlalchemy import insert
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, async_session_maker, engine

from src.admin.models import RoleOrm
from src.users.models import UserOrm
from src.stadiums.models import StadiumOrm
from src.stadiums.bookings.models import BookingOrm

from src.main import app as fastapi_app






#####################################? 88 probels ######################################
########################################################################################

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    role = open_mock_json("role")
    users = open_mock_json("users")
    stadiums = open_mock_json("stadiums")
    bookings = open_mock_json("bookings")

    for user in users:
        user["registred_at"] = datetime.strptime(user["registred_at"], "%Y-%m-%d")
    for booking in bookings:
        booking["date"] = datetime.strptime(booking["date"], "%Y-%m-%d")
        booking["hour_from"] = datetime.strptime(booking["hour_from"], "%H:%M")
        booking["hour_to"] = datetime.strptime(booking["hour_to"], "%H:%M")

    async with async_session_maker() as session:
        add_role = insert(RoleOrm).values(role)
        add_users = insert(UserOrm).values(users)
        add_stadiums = insert(StadiumOrm).values(stadiums)
        add_bookings = insert(BookingOrm).values(bookings)

        await session.execute(add_role)
        await session.execute(add_users)
        await session.execute(add_stadiums)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session") # session
async def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# httpx -> Fastapi app ni ishga tushirmasdan endpointlarni test qilish imkonini beradi:
# undan asinxronniy klientni olamiz, toza klient yaratamiz har safar.
@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# integratsionniy test uchun userni login qilib beradi
@pytest.fixture(scope="session")
async def authenticated_ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        assert ac.cookies[settings.COOKIE_NAME]
        yield ac

