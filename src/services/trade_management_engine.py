STOP_LOSS_PERCENT = 0.01

TAKE_PROFIT_PERCENT = 0.03

MAX_HOLD_BARS = 10


def should_exit_trade(
    entry_price,
    current_price,
    bars_held
):

    # -----------------------------------
    # Stop Loss
    # -----------------------------------

    stop_price = (
        entry_price
        * (1 - STOP_LOSS_PERCENT)
    )

    if current_price <= stop_price:

        return (
            True,
            "STOP_LOSS"
        )

    # -----------------------------------
    # Take Profit
    # -----------------------------------

    take_profit_price = (
        entry_price
        * (1 + TAKE_PROFIT_PERCENT)
    )

    if current_price >= take_profit_price:

        return (
            True,
            "TAKE_PROFIT"
        )

    # -----------------------------------
    # Time-Based Exit
    # -----------------------------------

    if bars_held >= MAX_HOLD_BARS:

        return (
            True,
            "MAX_HOLD_TIME"
        )

    return (
        False,
        None
    )


if __name__ == "__main__":

    examples = [
        (100, 98.5, 3),
        (100, 103.5, 2),
        (100, 100.2, 11),
        (100, 100.5, 4)
    ]

    print(
        "\n===== TRADE MANAGEMENT =====\n",
        flush=True
    )

    for entry, current, bars in examples:

        should_exit, reason = (
            should_exit_trade(
                entry,
                current,
                bars
            )
        )

        print(
            f"Entry={entry} | "
            f"Current={current} | "
            f"Bars={bars} | "
            f"Exit={should_exit} | "
            f"Reason={reason}",
            flush=True
        )