from src.db.database import SessionLocal
from src.db.models import MarketCandle


def replay_candles(
    ticker="AAPL",
    limit=50
):

    db = SessionLocal()

    try:

        candles = (
            db.query(MarketCandle)
            .filter(
                MarketCandle.ticker == ticker
            )
            .order_by(
                MarketCandle.timestamp.asc()
            )
            .limit(limit)
            .all()
        )

        print(
            f"Loaded {len(candles)} candles",
            flush=True
        )

        for candle in candles:

            replay_event = {
                "timestamp": candle.timestamp.isoformat(),
                "ticker": candle.ticker,

                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,

                "volume": candle.volume
            }

            print(
                replay_event,
                flush=True
            )

        return candles

    finally:
        db.close()


if __name__ == "__main__":
    replay_candles()