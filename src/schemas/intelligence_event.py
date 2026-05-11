from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class IntelligenceEvent(BaseModel):
    event_type: str
    symbol: Optional[str] = None
    source: str
    timestamp: datetime
    payload: Dict[str, Any]

