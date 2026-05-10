from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SignalData(BaseModel):

    ticker: str
    signal: str
    confidence: float


class SignalEvent(BaseModel):

    timestamp: datetime

    signal: SignalData

    action: str

    position: Optional[str] = None