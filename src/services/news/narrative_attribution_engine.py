from src.services.news.shared_regime_tracker import (
    shared_regime_tracker
)


class NarrativeAttributionEngine:

    def attribute_trade(
        self,
        trade_result,
        narrative_regime
    ):

        shared_regime_tracker.record_trade(
            narrative_regime,
            trade_result
        )

        if trade_result == "WIN":

            print(
                f"\nTrade success associated with "
                f"{narrative_regime}"
            )

        elif trade_result == "LOSS":

            print(
                f"\nTrade failure associated with "
                f"{narrative_regime}"
            )

        else:

            print(
                f"\nUnknown trade result "
                f"{trade_result} associated with "
                f"{narrative_regime}"
            )