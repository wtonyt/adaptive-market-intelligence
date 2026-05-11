from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean
)

from src.db.database import Base


class TradeOutcome(Base):

    __tablename__ = "trade_outcomes"

    trade_id = Column(
        String,
        primary_key=True
    )

    symbol = Column(String)

    entry_price = Column(Float)

    exit_price = Column(Float)

    pnl = Column(Float)

    duration_minutes = Column(Float)

    win = Column(Boolean)

    confidence_at_entry = Column(Float)

    market_regime = Column(String)