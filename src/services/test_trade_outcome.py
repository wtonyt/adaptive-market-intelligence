from src.db.crud_trade_outcome import (
    save_trade_outcome
)


test_outcome = {

    "trade_id": "TEST123",

    "symbol": "CUE",

    "entry_price": 4.25,

    "exit_price": 4.82,

    "pnl": 13.41,

    "duration_minutes": 22,

    "win": True,

    "confidence_at_entry": 0.90,

    "market_regime": "momentum"
}


save_trade_outcome(
    test_outcome
)