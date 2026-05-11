from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean
)

from src.db.database import Base


class ActivePosition(Base):

    __tablename__ = "active_positions"

    trade_id = Column(
        String,
        primary_key=True
    )

    symbol = Column(String)

    side = Column(String)

    entry_price = Column(Float)

    quantity = Column(Float)

    exposure = Column(Float)

    open = Column(Boolean)