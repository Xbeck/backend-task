import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# for redis
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
import uvicorn

from src.admin.auth import authentication_backend
from src.admin.views import UserAdmin, RoleAdmin, StadiumAdmin, BookingsAdmin

from src.database import engine
from src.users.auth.routers import router as router_auth
from src.admin.routers import router as router_admin
from src.users.routers import router as router_user
from src.stadiums.routers import router as router_stadium
from src.importer.routers import router as router_importer






#####################################? 88 probels ######################################
########################################################################################
# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
#     yield


app = FastAPI(
    title="Booking app",
    description="Fudbol maydonlarini bron qilish API",
    version="1.0.0",
    # lifespan=lifespan
)

app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_importer)
app.include_router(router_user)
app.include_router(router_stadium)



origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.mount("/static", StaticFiles(directory="src/static"), "static")


admin = Admin(
    app,
    engine,
    base_url="/admin",
    authentication_backend=authentication_backend,
)
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(StadiumAdmin)
admin.add_view(BookingsAdmin)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    # logger.info("Request handling time", extra={
    #     "process_time": round(process_time, 4)
    # })
    print(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))