import logging

from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker

class BaseDAO:
    model = None


    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none() 

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()


    @classmethod
    async def update(cls, **new_data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**new_data)
            await session.execute(stmt)
            await session.commit()


    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            await session.delete(query)
            await session.commit()


    @classmethod
    async def add_bulk(cls, *data):
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
            
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"
            print(msg, e)
            return None
