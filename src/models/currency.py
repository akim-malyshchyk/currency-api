from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
)
from managers.db_manager import Base
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String(255), nullable=False)
    date_ = Column(DateTime, unique=True, server_default=utcnow())
    price = Column(Numeric(precision=12, scale=5, asdecimal=False), nullable=False)

    def to_json(self) -> dict:
        return {
            "currency": self.currency,
            "price": self.price,
            "timestamp": self.date_.isoformat(timespec="seconds")
        }
