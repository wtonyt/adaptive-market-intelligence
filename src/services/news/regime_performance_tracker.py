class RegimePerformanceTracker:

    def __init__(self):

        self.performance = {}

    def record_trade(
        self,
        regime,
        outcome
    ):

        if regime not in self.performance:

            self.performance[regime] = {

                "wins": 0,

                "losses": 0
            }

        if outcome == "WIN":

            self.performance[
                regime
            ]["wins"] += 1

        elif outcome == "LOSS":

            self.performance[
                regime
            ]["losses"] += 1

    def summarize(self):

        summary = {}

        for regime, stats in (
            self.performance.items()
        ):

            total = (
                stats["wins"]
                +
                stats["losses"]
            )

            win_rate = (

                stats["wins"] / total

                if total > 0
                else 0
            )

            summary[regime] = {

                "wins":
                    stats["wins"],

                "losses":
                    stats["losses"],

                "win_rate":
                    round(win_rate, 2)
            }

        return summary