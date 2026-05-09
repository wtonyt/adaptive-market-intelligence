from src.db.database import SessionLocal
from src.db.models import SignalEvent, MarketCandle
from src.db.crud import save_agent_performance
from src.services.position_sizing_engine import (
    calculate_position_size
)

from src.services.market_regime_engine import (
    detect_market_regime
)
from src.services.trade_management_engine import (
    should_exit_trade
)
from src.models.portfolio_state import (
    PortfolioState
)

STARTING_CAPITAL = 10000
BACKTEST_SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA"
]
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

        portfolio = PortfolioState()

        positions = {}

        for symbol in BACKTEST_SYMBOLS:

            print(
                f"\n===== RUNNING BACKTEST FOR {symbol} =====",
                flush=True
            )

            candles = (
                db.query(MarketCandle)
                .filter(MarketCandle.ticker == symbol)
                .order_by(MarketCandle.timestamp.asc())
                .all()
            )

            symbol_events = [
                event for event in events
                if getattr(event, "ticker", None) == symbol
            ]

            regime = detect_market_regime()

            print(f"Backtest Regime: {regime}", flush=True)

            total_entries = 0
            closed_trades = 0
            winning_trades = 0
            losing_trades = 0

            print("\n===== BACKTEST START =====\n", flush=True)
            print(f"Loaded Events for {symbol}: {len(symbol_events)}", flush=True)
            print(f"Loaded Candles for {symbol}: {len(candles)}", flush=True)

            for event in symbol_events:

                current_price = find_nearest_candle_price(
                    event.timestamp,
                    candles
                )

                if current_price is None:
                    print(
                        f"Skipping event {event.id}: no candle price found",
                        flush=True
                    )
                    continue

                action = event.action

                if symbol in positions:
                    positions[symbol]["bars_held"] += 1

                # -----------------------------------
                # ENTER LONG
                # -----------------------------------

                if action == "ENTER_LONG" and symbol not in positions:

                    entry_price = apply_slippage(
                        current_price,
                        "BUY"
                    )

                    confidence_score = 0.80

                    position_percent = calculate_position_size(
                        confidence_score,
                        regime
                    )

                    position_size = (
                        portfolio.cash_balance * position_percent
                    )

                    if position_size <= 0:
                        print(
                            "Skipping trade due to zero position size",
                            flush=True
                        )
                        continue

                    shares = position_size / entry_price

                    positions[symbol] = {
                        "entry_price": entry_price,
                        "shares": shares,
                        "bars_held": 0
                    }

                    portfolio.add_position(
                        symbol=symbol,
                        shares=shares,
                        entry_price=entry_price,
                        position_value=position_size
                    )

                    portfolio.cash_balance -= COMMISSION_PER_TRADE

                    total_entries += 1

                    print(
                        f"Position %={round(position_percent, 4)} | "
                        f"Position Size=${round(position_size, 2)}",
                        flush=True
                    )

                    print(
                        f"\nENTER LONG {symbol} @ {round(entry_price, 2)}",
                        flush=True
                    )

                    print(
                        f"Shares: {round(shares, 4)}",
                        flush=True
                    )

                    print(
                        f"Capital After Commission: "
                        f"{round(portfolio.cash_balance, 2)}",
                        flush=True
                    )

                    continue

                # -----------------------------------
                # EXIT LONG
                # -----------------------------------

                if symbol in positions:

                    position = positions[symbol]

                    should_exit, exit_reason = should_exit_trade(
                        position["entry_price"],
                        current_price,
                        position["bars_held"]
                    )

                    if should_exit:

                        exit_price = apply_slippage(
                            current_price,
                            "SELL"
                        )

                        pnl = (
                            exit_price - position["entry_price"]
                        ) * position["shares"]

                        exit_value = (
                            position["shares"] * exit_price
                        )

                        portfolio.remove_position(
                            symbol=symbol,
                            exit_value=exit_value,
                            pnl=pnl
                        )

                        portfolio.cash_balance -= COMMISSION_PER_TRADE

                        closed_trades += 1

                        if pnl >= 0:
                            winning_trades += 1
                        else:
                            losing_trades += 1

                        print(
                            f"\nEXIT LONG {symbol} @ {round(exit_price, 2)}",
                            flush=True
                        )

                        print(f"Exit Reason: {exit_reason}", flush=True)
                        print(f"PnL: {round(pnl, 2)}", flush=True)
                        print(
                            f"Capital: {round(portfolio.cash_balance, 2)}",
                            flush=True
                        )

                        actual_outcome = (
                            "BUY"
                            if pnl > 0
                            else "SELL"
                        )

                        was_correct = pnl > 0

                        save_agent_performance(
                            agent_name="ML",
                            symbol=symbol,
                            prediction_side="BUY",
                            actual_outcome=actual_outcome,
                            confidence=0.82,
                            pnl=pnl,
                            was_correct=was_correct
                        )

                        save_agent_performance(
                            agent_name="RL",
                            symbol=symbol,
                            prediction_side="BUY",
                            actual_outcome=actual_outcome,
                            confidence=0.78,
                            pnl=pnl,
                            was_correct=was_correct
                        )

                        del positions[symbol]

            # -----------------------------------
            # RESULTS
            # -----------------------------------

            print("\n===== BACKTEST RESULTS =====", flush=True)
            print(f"Symbol: {symbol}", flush=True)
            print(f"Starting Capital: {STARTING_CAPITAL}", flush=True)
            print(
                f"Ending Capital: {round(portfolio.cash_balance, 2)}",
                flush=True
            )
            print(f"Entries: {total_entries}", flush=True)
            print(f"Closed Trades: {closed_trades}", flush=True)
            print(f"Wins: {winning_trades}", flush=True)
            print(f"Losses: {losing_trades}", flush=True)

            if closed_trades > 0:
                win_rate = (winning_trades / closed_trades) * 100
                print(f"Win Rate: {round(win_rate, 2)}%", flush=True)

            print("\n===== PORTFOLIO SUMMARY =====", flush=True)
            print(portfolio.summary(), flush=True)

            if symbol in positions:
                print(
                    f"\nOpen position remains for {symbol} "
                    f"at end of backtest",
                    flush=True
                )
                print(
                    f"Entry Price: "
                    f"{round(positions[symbol]['entry_price'], 2)}",
                    flush=True
                )

    finally:
        db.close()

if __name__ == "__main__":
    run_backtest()