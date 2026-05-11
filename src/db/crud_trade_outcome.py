from src.db.database import SessionLocal

from src.db.models_trade_outcome import (
    TradeOutcome
)


def save_trade_outcome(outcome):

    db = SessionLocal()

    try:

        record = TradeOutcome(
            trade_id=outcome["trade_id"],
            symbol=outcome["symbol"],
            entry_price=outcome["entry_price"],
            exit_price=outcome["exit_price"],
            pnl=outcome["pnl"],
            duration_minutes=outcome["duration_minutes"],
            win=outcome["win"],
            confidence_at_entry=outcome["confidence_at_entry"],
            market_regime=outcome["market_regime"]
        )

        db.merge(record)

        db.commit()

        print(
            "Saved trade outcome",
            flush=True
        )

    finally:

        db.close()