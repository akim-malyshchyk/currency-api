from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from managers.db_manager import Base


class UTCNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UTCNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):  # pylint: disable=unused-argument
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Currency(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String(255), nullable=False)
    date_ = Column(DateTime, unique=True, server_default=UTCNow())
    price = Column(Numeric(precision=12, scale=5, asdecimal=False), nullable=False)

    def to_json(self) -> dict:
        return {
            "currency": self.currency,
            "price": self.price,
            "timestamp": self.date_.isoformat(timespec="seconds")
        }
