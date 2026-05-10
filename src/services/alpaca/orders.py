from alpaca.trading.requests import (
    MarketOrderRequest
)

from alpaca.trading.enums import (
    OrderSide,
    TimeInForce
)

from src.services.alpaca.client import (
    get_trading_client
)


def submit_market_buy(symbol, qty):

    client = get_trading_client()

    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )

    order = client.submit_order(
        order_data=order_data
    )

    return order


def submit_market_sell(symbol, qty):

    client = get_trading_client()

    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )

    order = client.submit_order(
        order_data=order_data
    )

    return order