class PortfolioState:

    def __init__(self):

        # -----------------------------------
        # Portfolio Metrics
        # -----------------------------------

        self.cash_balance = 10000.0

        self.open_positions = {}

        self.realized_pnl = 0.0

        self.unrealized_pnl = 0.0

        self.total_exposure = 0.0

    # -----------------------------------
    # Add Position
    # -----------------------------------

    def add_position(
        self,
        symbol,
        shares,
        entry_price,
        position_value
    ):

        self.open_positions[symbol] = {
            "shares": shares,
            "entry_price": entry_price,
            "position_value": position_value
        }

        self.cash_balance -= position_value

        self.recalculate_exposure()

    # -----------------------------------
    # Remove Position
    # -----------------------------------

    def remove_position(
        self,
        symbol,
        exit_value,
        pnl
    ):

        if symbol not in self.open_positions:

            return

        self.cash_balance += exit_value

        self.realized_pnl += pnl

        del self.open_positions[symbol]

        self.recalculate_exposure()

    # -----------------------------------
    # Exposure Calculation
    # -----------------------------------

    def recalculate_exposure(self):

        deployed_capital = sum(
            position["position_value"]
            for position in (
                self.open_positions.values()
            )
        )

        total_equity = (
            self.cash_balance
            + deployed_capital
        )

        if total_equity <= 0:

            self.total_exposure = 0.0

            return

        self.total_exposure = (
            deployed_capital
            / total_equity
        )

    # -----------------------------------
    # Summary
    # -----------------------------------

    def summary(self):

        return {
            "cash_balance": round(
                self.cash_balance,
                2
            ),

            "open_positions": len(
                self.open_positions
            ),

            "realized_pnl": round(
                self.realized_pnl,
                2
            ),

            "total_exposure": round(
                self.total_exposure,
                4
            )
        }


if __name__ == "__main__":

    portfolio = PortfolioState()

    print(
        "\n===== INITIAL PORTFOLIO =====\n",
        flush=True
    )

    print(
        portfolio.summary(),
        flush=True
    )

    portfolio.add_position(
        symbol="AAPL",
        shares=10,
        entry_price=100,
        position_value=1000
    )

    print(
        "\n===== AFTER ENTRY =====\n",
        flush=True
    )

    print(
        portfolio.summary(),
        flush=True
    )

    portfolio.remove_position(
        symbol="AAPL",
        exit_value=1050,
        pnl=50
    )

    print(
        "\n===== AFTER EXIT =====\n",
        flush=True
    )

    print(
        portfolio.summary(),
        flush=True
    )