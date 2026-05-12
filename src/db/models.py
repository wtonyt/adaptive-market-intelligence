from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    Boolean,
    Text
)
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

class CopilotAnalysisRecord(Base):

    __tablename__ = "copilot_analysis_records"

    id = Column(String, primary_key=True)

    trade_id = Column(String, index=True)

    user_email = Column(String, index=True)

    symbol = Column(String, index=True)

    actionability = Column(String)

    confidence_score = Column(Float)

    summary = Column(Text)

    analysis_payload = Column(JSON)

    callback_url = Column(String, nullable=True)

    callback_sent = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class TradeEvent(Base):
    __tablename__ = "trade_events"

    id = Column(Integer, primary_key=True, index=True)

    trade_id = Column(String, index=True, nullable=True)
    provider = Column(String, index=True, nullable=False, default="nodeasset")
    source = Column(String, nullable=True)

    symbol = Column(String, index=True, nullable=True)
    side = Column(String, nullable=True)
    specialist = Column(String, nullable=True)

    confidence = Column(Float, nullable=True)
    price = Column(Float, nullable=True)

    event_timestamp = Column(DateTime(timezone=True), nullable=True)

    processing_state = Column(String, nullable=False, default="RECEIVED")
    execution_status = Column(String, nullable=False, default="NOT_EXECUTED")

    raw_payload = Column(JSON, nullable=True)
    normalized_payload = Column(JSON, nullable=True)

    approved_at = Column(DateTime(timezone=True), nullable=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)

    failure_reason = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

class StructuralFailureEvent(Base):

    __tablename__ = "structural_failure_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    trade_id = Column(
        String,
        index=True
    )

    symbol = Column(
        String,
        index=True
    )

    failure_pattern = Column(
        String,
        index=True
    )

    severity = Column(Float)

    blocked = Column(Boolean)

    reasons = Column(JSON)

    raw_context = Column(JSON)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

class StructuralOutcomeEvaluation(Base):
        
    __tablename__ = "structural_outcome_evaluations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    trade_id = Column(
        String,
        index=True
    )

    symbol = Column(
        String,
        index=True
    )

    failure_pattern = Column(
        String,
        index=True
    )

    blocked = Column(Boolean)

    entry_price = Column(Float)

    evaluation_price = Column(Float)

    pnl_delta_pct = Column(Float)

    outcome = Column(String)

    correct_veto = Column(Boolean)

    evaluation_notes = Column(Text)

    evaluated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )