import os

from dotenv import load_dotenv

from alpaca.trading.client import TradingClient

load_dotenv()

client = TradingClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY"),
    paper=True
)

orders = client.get_orders()

print("\n--- ORDERS ---\n")

for order in orders:

    print(f"Symbol: {order.symbol}")
    print(f"Status: {order.status}")
    print(f"Qty: {order.qty}")
    print(f"Side: {order.side}")
    print(f"Order Type: {order.order_type}")
    print("---")