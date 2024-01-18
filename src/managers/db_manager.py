import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiohttp.web import HTTPInternalServerError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
)
from dotenv import load_dotenv


load_dotenv()
Base = declarative_base()


class SingletonDBManager(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBaseError(Exception):
    pass


class DBManager(metaclass=SingletonDBManager):
    def __init__(self):
        self.db_url = ''.join((
            'postgresql+asyncpg://',
            f'{os.getenv("DB_USERNAME")}',
            f':{os.getenv("DB_PASSWORD")}',
            f'@{os.getenv("DB_HOST")}',
            f':{os.getenv("DB_PORT")}',
            f'/{os.getenv("DB_NAME")}'
        ))
        self.pool_size = int(os.getenv("POOL_SIZE", "20"))
        self.max_overflow = int(os.getenv("MAX_OVERFLOW", "5"))
        self.pool_recycle = int(os.getenv("POOL_RECYCLE", "60"))
        self._async_engine = None
        self._async_session = None

    async def __aenter__(self):
        self._async_session = await self.async_session()
        return self._async_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_session.close()

    async def async_engine(self) -> AsyncEngine:
        try:
            if self._async_engine is None:
                self._async_engine = create_async_engine(
                    self.db_url,
                    future=True,
                    pool_size=self.pool_size,
                    max_overflow=self.max_overflow,
                    pool_recycle=self.pool_recycle,
                    pool_timeout=10,
                    pool_pre_ping=True,
                )
            return self._async_engine
        except SQLAlchemyError as err:
            raise HTTPInternalServerError(text="Error creating async engine") from err

    async def async_session(self) -> AsyncSession:
        return scoped_session(sessionmaker(bind=await self.async_engine(),
                                           class_=AsyncSession,
                                           expire_on_commit=False,
                                           autoflush=False,
                                           autocommit=False))()


db_manager = DBManager()


@asynccontextmanager
async def get_async_session():
    db = await db_manager.async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session() as db:
        yield db
