from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime

from src.db.database import Base


class NarrativeEventRecord(Base):

    __tablename__ = "narrative_events"

    id = Column(String, primary_key=True)

    event_type = Column(String)

    sentiment = Column(String)

    symbol = Column(String)

    source = Column(String)

    payload = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)