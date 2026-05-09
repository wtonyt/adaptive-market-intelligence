import os

from polygon import RESTClient
from dotenv import load_dotenv
from src.db.crud import save_market_candles

load_dotenv()

API_KEY = os.getenv("POLYGON_API_KEY")

client = RESTClient(API_KEY)


def fetch_aggregates(
    ticker="AAPL",
    multiplier=1,
    timespan="minute",
    from_date="2025-01-01",
    to_date="2025-01-05"
):

    print(
        f"Fetching Polygon aggregates for {ticker}",
        flush=True
    )

    aggs = client.get_aggs(
        ticker=ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=from_date,
        to=to_date,
        limit=50000
    )

    candles = []

    for agg in aggs:

        candles.append({
            "timestamp": agg.timestamp,
            "open": agg.open,
            "high": agg.high,
            "low": agg.low,
            "close": agg.close,
            "volume": agg.volume
        })

    print(
        f"Retrieved {len(candles)} candles",
        flush=True
    )

    return candles


if __name__ == "__main__":

    candles = fetch_aggregates()

    save_market_candles(
        ticker="AAPL",
        candles=candles
    )