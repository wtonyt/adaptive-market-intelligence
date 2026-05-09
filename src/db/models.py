from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from sqlalchemy import Boolean
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

class ConsensusEvent(Base):

    __tablename__ = "consensus_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    symbol = Column(
        String,
        index=True
    )

    ml_side = Column(String)

    rl_side = Column(String)

    consensus = Column(Boolean)

    consensus_score = Column(Float)

    final_side = Column(String)

    confidence_score = Column(Float)

    reason = Column(String)

    timestamp = Column(
        DateTime,
        index=True
    )

class AgentPerformance(Base):

    __tablename__ = "agent_performance"

    id = Column(Integer, primary_key=True, index=True)

    agent_name = Column(String, index=True)  # ML or RL
    symbol = Column(String, index=True)

    prediction_side = Column(String)
    actual_outcome = Column(String)

    confidence = Column(Float)
    pnl = Column(Float)

    was_correct = Column(Boolean)

    timestamp = Column(DateTime, index=True)