from pydantic import BaseModel


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

    data: CoPilotTradeData