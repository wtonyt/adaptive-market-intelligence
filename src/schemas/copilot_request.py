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


class CoPilotRequest(
    BaseModel
):

    type: str

    user_email: str

    callback_url: Optional[str] = None

    data: CoPilotTradeData