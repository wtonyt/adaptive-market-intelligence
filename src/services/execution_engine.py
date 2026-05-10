from src.services.alpaca.orders import (
    submit_market_buy,
    submit_market_sell
)


def execute_trade(signal):

    symbol = signal["symbol"]
    side = signal["side"]
    quantity = signal["quantity"]

    if side == "BUY":

        order = submit_market_buy(
            symbol=symbol,
            qty=quantity
        )

    elif side == "SELL":

        order = submit_market_sell(
            symbol=symbol,
            qty=quantity
        )

    else:
        raise ValueError("Invalid trade side")

    return order