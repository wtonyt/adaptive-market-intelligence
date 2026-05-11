from src.db.database import SessionLocal

from src.db.models_decision import (
    DecisionRecord
)

from src.db.models_trade_outcome import (
    TradeOutcome
)


class PerformanceAnalyzer:

    def analyze(self):

        db = SessionLocal()

        try:

            decisions = db.query(
                DecisionRecord
            ).all()

            outcomes = db.query(
                TradeOutcome
            ).all()

            outcome_map = {
                o.trade_id: o
                for o in outcomes
            }

            total = 0
            wins = 0

            confidence_buckets = {
                "high": [],
                "medium": [],
                "low": []
            }

            for decision in decisions:

                outcome = outcome_map.get(
                    decision.trade_id
                )

                if not outcome:
                    continue

                total += 1

                if outcome.win:
                    wins += 1

                if decision.confidence >= 0.80:
                    confidence_buckets["high"].append(
                        outcome.win
                    )

                elif decision.confidence >= 0.60:
                    confidence_buckets["medium"].append(
                        outcome.win
                    )

                else:
                    confidence_buckets["low"].append(
                        outcome.win
                    )

            overall_win_rate = (
                wins / total
                if total > 0 else 0
            )

            print("\n--- PERFORMANCE ANALYSIS ---")

            print(
                f"Total Trades: {total}"
            )

            print(
                f"Overall Win Rate: "
                f"{round(overall_win_rate * 100, 2)}%"
            )

            for bucket, values in confidence_buckets.items():

                if values:

                    rate = (
                        sum(values) / len(values)
                    ) * 100

                    print(
                        f"{bucket.upper()} confidence "
                        f"win rate: "
                        f"{round(rate, 2)}%"
                    )

        finally:

            db.close()