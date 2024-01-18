import os
from aiohttp.web import HTTPInternalServerError
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from managers.db_manager import DBManager, get_async_session
from models.currency import Currency


class CurrencyDBManager:
    def __init__(self):
        self.db_manager = DBManager()

    async def _save(self, session: AsyncSession, currency: str, last_price: float) -> Currency:
        instance = Currency(currency=currency, price=last_price)
        session.add(instance)
        await session.commit()
        return instance

    async def save_currency(self, currency: str, last_price: float) -> dict:
        try:
            async with get_async_session() as session:
                instance = await self._save(session, currency, last_price)
                data = instance.to_json()
        except (SQLAlchemyError, OSError)  as err:
            raise HTTPInternalServerError(text='Error saving currency price') from err
        return data

    async def get_history(self, page: int = 1) -> list[dict]:
        try:
            page_size = int(os.getenv("PAGE_SIZE", "10"))
            offset = max((page - 1) * page_size, 0)
            limit = offset + page_size

            async with get_async_session() as session:
                query = select(Currency).order_by(Currency.date_).limit(limit).offset(offset)
                history = await session.scalars(query)
                data = [currency.to_json() for currency in history]

        except (ValueError, SQLAlchemyError, OSError) as err:
            raise HTTPInternalServerError(text='Error getting price history') from err

        return data

    async def delete_history(self) -> None:
        try:
            async with get_async_session() as session:
                truncate_statement = text(f'TRUNCATE TABLE {Currency.__tablename__}')
                await session.execute(truncate_statement)
                await session.commit()
        except (SQLAlchemyError, OSError) as err:
            raise HTTPInternalServerError(text='Error deleting price history') from err
