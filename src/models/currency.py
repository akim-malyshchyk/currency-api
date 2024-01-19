from datetime import datetime
from sqlalchemy import (
    DateTime,
    Numeric,
    String,
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
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
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    currency: Mapped[str] = mapped_column(String(255), nullable=False)
    date_: Mapped[datetime] = mapped_column(unique=True, server_default=UTCNow(), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(precision=12, scale=5, asdecimal=False), nullable=False)

    def to_json(self) -> dict:
        return {
            "currency": self.currency,
            "price": self.price,
            "timestamp": self.date_.isoformat(timespec="seconds")
        }
