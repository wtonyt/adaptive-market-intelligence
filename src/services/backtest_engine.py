from src.db.database import SessionLocal
from src.db.models import SignalEvent


STARTING_CAPITAL = 10000


def run_backtest():

    db = SessionLocal()

    try:

        events = (
            db.query(SignalEvent)
            .order_by(SignalEvent.timestamp.asc())
            .all()
        )

        capital = STARTING_CAPITAL

        current_position = None
        entry_price = None

        simulated_price = 100.0

        total_trades = 0
        winning_trades = 0
        losing_trades = 0

        print("\n===== BACKTEST START =====\n", flush=True)

        for event in events:

            # Fake market movement
            simulated_price += 1.5

            action = event.action

            if action == "ENTER_LONG":

                if current_position is None:

                    current_position = "LONG"
                    entry_price = simulated_price

                    total_trades += 1

                    print(
                        f"ENTER LONG @ {entry_price}",
                        flush=True
                    )

            elif action == "EXIT_LONG":

                if current_position == "LONG":

                    exit_price = simulated_price

                    pnl = exit_price - entry_price

                    capital += pnl

                    if pnl >= 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1

                    print(
                        f"EXIT LONG @ {exit_price} "
                        f"PnL={round(pnl, 2)} "
                        f"Capital={round(capital, 2)}",
                        flush=True
                    )

                    current_position = None
                    entry_price = None

        print("\n===== BACKTEST RESULTS =====", flush=True)

        print(f"Starting Capital: {STARTING_CAPITAL}", flush=True)
        print(f"Ending Capital: {round(capital, 2)}", flush=True)

        print(f"Total Trades: {total_trades}", flush=True)
        print(f"Wins: {winning_trades}", flush=True)
        print(f"Losses: {losing_trades}", flush=True)

        if total_trades > 0:

            win_rate = (
                winning_trades / total_trades
            ) * 100

            print(
                f"Win Rate: {round(win_rate, 2)}%",
                flush=True
            )

    finally:
        db.close()


if __name__ == "__main__":
    run_backtest()