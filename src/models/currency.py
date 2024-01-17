from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    func,
)
from models.base import Base


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, nullable=False)
    date_ = Column(DateTime, default=func.now())
    price = Column(Numeric)


sa_currency = Currency.__table__
