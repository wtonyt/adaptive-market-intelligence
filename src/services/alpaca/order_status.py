from src.services.alpaca.client import (
    get_trading_client
)


def get_order(order_id):

    client = get_trading_client()

    return client.get_order_by_id(order_id)