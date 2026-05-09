from src.db.database import SessionLocal
from src.db.models import SignalEvent, MarketCandle
from src.db.crud import save_agent_performance
from src.services.position_sizing_engine import (
    calculate_position_size
)

from src.services.market_regime_engine import (
    detect_market_regime
)

STARTING_CAPITAL = 10000

COMMISSION_PER_TRADE = 1.00
SLIPPAGE_BPS = 5

def apply_slippage(price, side):

    slippage_multiplier = SLIPPAGE_BPS / 10000

    if side == "BUY":
        return price * (1 + slippage_multiplier)

    elif side == "SELL":
        return price * (1 - slippage_multiplier)

    return price


def find_nearest_candle_price(event_timestamp, candles):
    """
    Find the closest candle at or before the event timestamp.
    """

    matching_candles = [
        candle for candle in candles
        if candle.timestamp <= event_timestamp
    ]

    if not matching_candles:
        return None

    return matching_candles[-1].close


def run_backtest():

    db = SessionLocal()

    try:

        events = (
            db.query(SignalEvent)
            .order_by(SignalEvent.timestamp.asc())
            .all()
        )

        candles = (
            db.query(MarketCandle)
            .filter(MarketCandle.ticker == "AAPL")
            .order_by(MarketCandle.timestamp.asc())
            .all()
        )

        capital = STARTING_CAPITAL

        regime = detect_market_regime()

        print(
            f"Backtest Regime: {regime}",
            flush=True
        )

        current_position = None

        entry_price = None
        shares = None

        total_entries = 0
        closed_trades = 0

        winning_trades = 0
        losing_trades = 0

        print("\n===== BACKTEST START =====\n", flush=True)

        print(f"Loaded Events: {len(events)}", flush=True)
        print(f"Loaded Candles: {len(candles)}", flush=True)

        for event in events:

            current_price = find_nearest_candle_price(
                event.timestamp,
                candles
            )

            if current_price is None:

                print(
                    f"Skipping event {event.id}: "
                    f"no candle price found",
                    flush=True
                )

                continue

            action = event.action

            # -----------------------------------
            # ENTER LONG
            # -----------------------------------

            if action == "ENTER_LONG":

                if current_position is None:

                    current_position = "LONG"

                    entry_price = apply_slippage(
                        current_price,
                        "BUY"
                    )

                    confidence_score = 0.80

                    position_percent = (
                        calculate_position_size(
                            confidence_score,
                            regime
                        )
                    )

                    position_size = (
                        capital * position_percent
                    )
                    if position_size <= 0:

                        print(
                            "Skipping trade due to zero position size",
                            flush=True
                        )

                        continue

                    shares = (
                        position_size / entry_price
                    )

                    print(
                        f"Position %={round(position_percent, 4)} | "
                        f"Position Size=${round(position_size, 2)}",
                        flush=True
                    )
                    
                    capital -= (
                        position_size +
                        COMMISSION_PER_TRADE
                    )

                    total_entries += 1

                    print(
                        f"\nENTER LONG @ "
                        f"{round(entry_price, 2)}",
                        flush=True
                    )

                    print(
                        f"Shares: {round(shares, 4)}",
                        flush=True
                    )

                    print(
                        f"Capital After Commission: "
                        f"{round(capital, 2)}",
                        flush=True
                    )

            # -----------------------------------
            # EXIT LONG
            # -----------------------------------

            elif action == "EXIT_LONG":

                if current_position == "LONG":

                    exit_price = apply_slippage(
                        current_price,
                        "SELL"
                    )

                    capital -= COMMISSION_PER_TRADE

                    pnl = (
                        exit_price - entry_price
                    ) * shares

                    capital += (
                        shares * exit_price
                    )
                    
                    actual_outcome = (
                        "BUY"
                        if pnl > 0
                        else "SELL"
                    )

                    was_correct = pnl > 0

                    # ML performance
                    save_agent_performance(
                        agent_name="ML",

                        symbol="AAPL",

                        prediction_side="BUY",

                        actual_outcome=actual_outcome,

                        confidence=0.82,

                        pnl=pnl,

                        was_correct=was_correct
                    )

                    # RL performance
                    save_agent_performance(
                        agent_name="RL",

                        symbol="AAPL",

                        prediction_side="BUY",

                        actual_outcome=actual_outcome,

                        confidence=0.78,

                        pnl=pnl,

                        was_correct=was_correct
                    )
                    closed_trades += 1

                    if pnl >= 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1

                    print(
                        f"\nEXIT LONG @ "
                        f"{round(exit_price, 2)}",
                        flush=True
                    )

                    print(
                        f"PnL: {round(pnl, 2)}",
                        flush=True
                    )

                    print(
                        f"Capital: {round(capital, 2)}",
                        flush=True
                    )

                    current_position = None

                    entry_price = None
                    shares = None

        # -----------------------------------
        # RESULTS
        # -----------------------------------

        print("\n===== BACKTEST RESULTS =====", flush=True)

        print(
            f"Starting Capital: "
            f"{STARTING_CAPITAL}",
            flush=True
        )

        print(
            f"Ending Capital: "
            f"{round(capital, 2)}",
            flush=True
        )

        print(
            f"Entries: {total_entries}",
            flush=True
        )

        print(
            f"Closed Trades: {closed_trades}",
            flush=True
        )

        print(
            f"Wins: {winning_trades}",
            flush=True
        )

        print(
            f"Losses: {losing_trades}",
            flush=True
        )

        if closed_trades > 0:

            win_rate = (
                winning_trades / closed_trades
            ) * 100

            print(
                f"Win Rate: "
                f"{round(win_rate, 2)}%",
                flush=True
            )

        if current_position == "LONG":

            print(
                f"\nOpen position remains "
                f"at end of backtest",
                flush=True
            )

            print(
                f"Entry Price: "
                f"{round(entry_price, 2)}",
                flush=True
            )

    finally:
        db.close()


if __name__ == "__main__":
    run_backtest()