from pydantic import BaseModel
from typing import Optional


class CoPilotTradeData(
    BaseModel
):

    trade_id: str

    specialist: str

    symbol: str

    side: str

    quantity: int

    price: float

    timestamp: str

    avg_liq: Optional[float] = None

    min_liq: Optional[float] = None

    avg_bad_p: Optional[float] = None

    float_size: Optional[float] = None


class CoPilotRequest(
    BaseModel
):

    type: str

    user_email: str

    callback_url: Optional[str] = None

    data: CoPilotTradeData