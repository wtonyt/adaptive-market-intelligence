import os
from datetime import datetime

from dotenv import load_dotenv

from alpaca.trading.client import (
    TradingClient
)

from src.services.decision_engine.trade_management_engine import (
    TradeManagementEngine
)

load_dotenv()


class PositionMonitor:

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

        self.trade_manager = (
            TradeManagementEngine()
        )

    def monitor_positions(self):

        positions = (
            self.client.get_all_positions()
        )

        print(
            "\n--- POSITION MONITOR ---\n"
        )

        for position in positions:

            unrealized_pnl_pct = float(
                position.unrealized_plpc
            ) * 100

            position_data = {

                "symbol": position.symbol,

                "unrealized_pnl": (
                    unrealized_pnl_pct
                ),

                "duration_minutes": 15
            }

            actions = (
                self.trade_manager
                .evaluate_position(
                    position_data
                )
            )

            print(
                f"Symbol: "
                f"{position.symbol}"
            )

            print(
                f"PnL %: "
                f"{round(unrealized_pnl_pct, 2)}"
            )

            print(
                f"Actions: "
                f"{actions}"
            )

            print("---")