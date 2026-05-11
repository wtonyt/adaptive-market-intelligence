from src.services.decision_engine.trade_management_engine import (
    TradeManagementEngine
)

engine = TradeManagementEngine()

test_position = {

    "symbol": "AAPL",

    "unrealized_pnl": 6.4,

    "duration_minutes": 18
}

actions = engine.evaluate_position(
    test_position
)

print(actions)