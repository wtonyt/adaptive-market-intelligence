from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IntelligenceEvent(BaseModel):

    event_type: str

    symbol: Optional[str]

    source: str

    timestamp: datetime

    payload: dict