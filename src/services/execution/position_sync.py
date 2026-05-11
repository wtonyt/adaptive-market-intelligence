import os

from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

from src.db.crud_positions import upsert_active_position

load_dotenv()


class PositionSync:

    def __init__(self):

        self.client = TradingClient(
            api_key=os.getenv("ALPACA_API_KEY"),
            secret_key=os.getenv("ALPACA_SECRET_KEY"),
            paper=True
        )

    def sync_positions(self):

        positions = self.client.get_all_positions()

        print("\n--- BROKER POSITIONS ---\n")

        for position in positions:

            position_data = {
                "trade_id": f"ALPACA-{position.symbol}",
                "symbol": position.symbol,
                "side": "LONG" if float(position.qty) > 0 else "SHORT",
                "entry_price": float(position.avg_entry_price),
                "quantity": float(position.qty),
                "exposure": float(position.market_value),
                "open": True,
            }

            print(position_data)

            upsert_active_position(position_data)