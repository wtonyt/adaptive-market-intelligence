from dotenv import load_dotenv

load_dotenv()

from src.services.execution_engine import (
    execute_trade
)

signal = {
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 1
}

result = execute_trade(signal)

print(result)