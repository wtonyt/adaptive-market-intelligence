from pydantic import BaseModel

from datetime import datetime

from typing import Optional


class TraderSignal(BaseModel):

    source: str

    symbol: str

    side: str

    confidence: float

    timestamp: datetime

    suggested_price: Optional[float] = None

    liquidity_score: Optional[float] = None

    timing_score: Optional[float] = None

    metadata: Optional[dict] = None


class ConsensusSignal(BaseModel):

    symbol: str

    ml_side: Optional[str] = None

    rl_side: Optional[str] = None

    consensus: bool

    consensus_score: float

    final_side: str

    confidence_score: float

    reason: str

    timestamp: datetime