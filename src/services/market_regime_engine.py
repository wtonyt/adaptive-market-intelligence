import statistics

from src.db.database import SessionLocal
from src.db.models import MarketCandle


TREND_THRESHOLD = 0.01

VOLATILITY_THRESHOLD = 0.02


def calculate_returns(prices):

    returns = []

    for i in range(1, len(prices)):

        prev_price = prices[i - 1]

        current_price = prices[i]

        pct_return = (
            (current_price - prev_price)
            / prev_price
        )

        returns.append(pct_return)

    return returns


def detect_market_regime():

    db = SessionLocal()

    try:

        candles = (
            db.query(MarketCandle)
            .filter(
                MarketCandle.ticker == "AAPL"
            )
            .order_by(
                MarketCandle.timestamp.asc()
            )
            .limit(100)
            .all()
        )

        if len(candles) < 20:

            print(
                "Not enough candle data",
                flush=True
            )

            return "UNKNOWN"

        prices = [
            candle.close
            for candle in candles
        ]

        returns = calculate_returns(prices)

        avg_return = (
            sum(returns) / len(returns)
        )

        volatility = (
            statistics.stdev(returns)
        )

        # -----------------------------------
        # Regime Logic
        # -----------------------------------

        if abs(avg_return) > TREND_THRESHOLD:

            regime = "TRENDING"

        elif volatility > VOLATILITY_THRESHOLD:

            regime = "VOLATILE"

        else:

            regime = "NEUTRAL"

        print(
            "\n===== MARKET REGIME =====\n",
            flush=True
        )

        print(
            f"Average Return: "
            f"{round(avg_return, 6)}",
            flush=True
        )

        print(
            f"Volatility: "
            f"{round(volatility, 6)}",
            flush=True
        )

        print(
            f"Detected Regime: "
            f"{regime}",
            flush=True
        )

        return regime

    finally:

        db.close()


if __name__ == "__main__":

    detect_market_regime()