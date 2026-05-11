from sqlalchemy import Column, String, Float, Boolean, JSON
from src.db.database import Base


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    trade_id = Column(String, primary_key=True)
    symbol = Column(String)

    action = Column(String)

    confidence = Column(Float)
    risk_score = Column(Float)

    approved = Column(Boolean)

    reasons = Column(JSON)
    blockers = Column(JSON)