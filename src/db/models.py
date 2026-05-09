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