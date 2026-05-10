import os

from alpaca.trading.client import TradingClient


def get_trading_client():

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    client = TradingClient(
        api_key=api_key,
        secret_key=secret_key,
        paper=True
    )

    return client