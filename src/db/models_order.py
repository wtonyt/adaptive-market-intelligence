from sqlalchemy import (
    Column,
    String,
    Float
)

from src.db.database import Base


class OrderRecord(Base):

    __tablename__ = "order_records"

    order_id = Column(
        String,
        primary_key=True
    )

    trade_id = Column(String)

    symbol = Column(String)

    status = Column(String)

    qty = Column(Float)

    filled_qty = Column(Float)

    side = Column(String)