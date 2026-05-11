class TradeManagementEngine:

    def evaluate_position(
        self,
        position_data
    ):

        actions = []

        unrealized_pnl = position_data.get(
            "unrealized_pnl",
            0
        )

        duration_minutes = position_data.get(
            "duration_minutes",
            0
        )

        # Stop loss logic
        if unrealized_pnl <= -2.0:

            actions.append(
                "EXIT_POSITION_STOP_LOSS"
            )

        # Profit protection
        elif unrealized_pnl >= 5.0:

            actions.append(
                "TAKE_PROFIT"
            )

        # Time decay exit
        elif duration_minutes > 60:

            actions.append(
                "TIME_BASED_EXIT"
            )

        return actions