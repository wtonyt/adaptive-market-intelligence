def calculate_position_size(
    confidence_score,
    regime
):

    # -----------------------------------
    # Base Size
    # -----------------------------------

    if confidence_score >= 0.90:

        base_size = 0.20

    elif confidence_score >= 0.75:

        base_size = 0.10

    elif confidence_score >= 0.60:

        base_size = 0.05

    else:

        base_size = 0.00

    # -----------------------------------
    # Regime Adjustments
    # -----------------------------------

    if regime == "VOLATILE":

        base_size *= 0.50

    elif regime == "TRENDING":

        base_size *= 1.25

    # -----------------------------------
    # Safety Cap
    # -----------------------------------

    base_size = min(
        base_size,
        0.25
    )

    return round(
        base_size,
        4
    )


if __name__ == "__main__":

    examples = [
        (0.92, "TRENDING"),
        (0.78, "NEUTRAL"),
        (0.62, "VOLATILE"),
        (0.40, "NEUTRAL")
    ]

    print(
        "\n===== POSITION SIZING =====\n",
        flush=True
    )

    for confidence, regime in examples:

        size = calculate_position_size(
            confidence,
            regime
        )

        print(
            f"Confidence={confidence} | "
            f"Regime={regime} | "
            f"Position Size={size}",
            flush=True
        )