from src.db.database import SessionLocal
from src.db.models import SignalEvent
from datetime import datetime, timezone
from src.db.models import ConsensusEvent
from src.db.models import MarketCandle


def save_signal_event(data: dict):

    db = SessionLocal()

    try:

        signal = data.get("signal", {})

        event = SignalEvent(
            ticker=signal.get("ticker"),
            signal=signal.get("signal"),
            confidence=signal.get("confidence"),
            action=data.get("action"),
            position=data.get("position"),
            timestamp=data.get("timestamp")
        )

        db.add(event)
        db.commit()

        print("Saved event to PostgreSQL", flush=True)

    finally:
        db.close()

def save_market_candles(
    ticker: str,
    candles: list
):

    db = SessionLocal()

    try:

        inserted = 0

        for candle in candles:

            existing = (
                db.query(MarketCandle)
                .filter(
                    MarketCandle.ticker == ticker,
                    MarketCandle.timestamp == datetime.fromtimestamp(
                        candle["timestamp"] / 1000,
                        tz=timezone.utc
                    )
                )
                .first()
            )

            if existing:
                continue

            row = MarketCandle(
                ticker=ticker,

                timestamp=datetime.fromtimestamp(
                    candle["timestamp"] / 1000,
                    tz=timezone.utc
                ),

                open=candle["open"],
                high=candle["high"],
                low=candle["low"],
                close=candle["close"],

                volume=candle["volume"]
            )

            db.add(row)

            inserted += 1

        db.commit()

        print(
            f"Inserted {inserted} candles",
            flush=True
        )

    finally:
        db.close()

def save_consensus_event(
    consensus_signal
):

    db = SessionLocal()

    try:

        row = ConsensusEvent(

            symbol=consensus_signal.symbol,

            ml_side=consensus_signal.ml_side,

            rl_side=consensus_signal.rl_side,

            consensus=consensus_signal.consensus,

            consensus_score=(
                consensus_signal.consensus_score
            ),

            final_side=(
                consensus_signal.final_side
            ),

            confidence_score=(
                consensus_signal.confidence_score
            ),

            reason=consensus_signal.reason,

            timestamp=(
                consensus_signal.timestamp
            )
        )

        db.add(row)

        db.commit()

        print(
            "Consensus event saved",
            flush=True
        )

    finally:
        db.close()