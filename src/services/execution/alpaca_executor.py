import os

from alpaca.trading.client import (
    TradingClient
)

from alpaca.trading.requests import (
    MarketOrderRequest
)

from alpaca.trading.enums import (
    OrderSide,
    TimeInForce
)
from src.db.crud_orders import (
    upsert_order
)
from dotenv import load_dotenv

load_dotenv()


class AlpacaExecutor:

    def __init__(self):

        self.client = TradingClient(

            api_key=os.getenv(
                "ALPACA_API_KEY"
            ),

            secret_key=os.getenv(
                "ALPACA_SECRET_KEY"
            ),

            paper=True
        )

    def execute_trade(
        self,
        decision
    ):

        if not decision.approved:

            print(
                "Trade not approved"
            )

            return None

        try:

            order = (
                MarketOrderRequest(

                    symbol=decision.symbol,

                    qty=1,

                    side=OrderSide.BUY,

                    time_in_force=(
                        TimeInForce.DAY
                    )
                )
            )

            response = (
                self.client.submit_order(
                    order_data=order
                )
            )

            order_data = {

                "order_id": str(response.id),

                "trade_id": decision.trade_id,

                "symbol": decision.symbol,

                "status": str(response.status),

                "qty": float(response.qty),

                "filled_qty": float(
                    response.filled_qty or 0
                ),

                "side": str(response.side)
            }

            upsert_order(order_data)

            print(
                f"Order submitted: "
                f"{response.id}"
            )

            return response

        except Exception as e:

            print(
                f"Execution error: {e}"
            )

            return None