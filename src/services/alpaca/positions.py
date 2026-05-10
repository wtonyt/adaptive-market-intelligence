from src.services.alpaca.client import (
    get_trading_client
)


def get_all_positions():

    client = get_trading_client()

    return client.get_all_positions()


def close_position(symbol):

    client = get_trading_client()

    return client.close_position(symbol)