from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone

from src.db.database import Base


class SignalEvent(Base):

    __tablename__ = "signal_events"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String)
    signal = Column(String)

    confidence = Column(Float)

    action = Column(String)
    position = Column(String)

    timestamp = Column(DateTime)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

class MarketCandle(Base):

    __tablename__ = "market_candles"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True)

    timestamp = Column(DateTime, index=True)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    volume = Column(Float)