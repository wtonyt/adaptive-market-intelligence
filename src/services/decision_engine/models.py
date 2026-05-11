from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SignalContext(BaseModel):
    trade_id: str
    symbol: str
    timestamp: datetime

    signal_type: str
    signal_score: float

    current_price: float
    volume_ratio: Optional[float] = None
    vwap_distance: Optional[float] = None
    volatility_score: Optional[float] = None
    market_regime: Optional[str] = None

    already_in_position: bool = False


class DecisionResult(BaseModel):
    trade_id: str
    symbol: str
    action: str

    confidence: float
    risk_score: float
    approved: bool

    reasons: List[str]
    blockers: List[str]