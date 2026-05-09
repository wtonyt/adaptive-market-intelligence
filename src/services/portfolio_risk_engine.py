MAX_OPEN_POSITIONS = 3

MAX_PORTFOLIO_EXPOSURE = 0.50


def can_open_new_position(
    current_open_positions,
    current_exposure,
    proposed_position_size
):

    # -----------------------------------
    # Position Count Limit
    # -----------------------------------

    if (
        current_open_positions
        >= MAX_OPEN_POSITIONS
    ):

        return (
            False,
            "MAX_OPEN_POSITIONS"
        )

    # -----------------------------------
    # Exposure Limit
    # -----------------------------------

    projected_exposure = (
        current_exposure
        + proposed_position_size
    )

    if (
        projected_exposure
        > MAX_PORTFOLIO_EXPOSURE
    ):

        return (
            False,
            "MAX_PORTFOLIO_EXPOSURE"
        )

    return (
        True,
        None
    )


if __name__ == "__main__":

    examples = [
        (1, 0.20, 0.10),
        (3, 0.30, 0.05),
        (2, 0.45, 0.10),
        (1, 0.15, 0.05)
    ]

    print(
        "\n===== PORTFOLIO RISK ENGINE =====\n",
        flush=True
    )

    for positions, exposure, proposed in examples:

        allowed, reason = (
            can_open_new_position(
                positions,
                exposure,
                proposed
            )
        )

        print(
            f"Positions={positions} | "
            f"Exposure={exposure} | "
            f"Proposed={proposed} | "
            f"Allowed={allowed} | "
            f"Reason={reason}",
            flush=True
        )