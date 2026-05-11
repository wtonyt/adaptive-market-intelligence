class AlternativeDataEngine:

    def evaluate(
        self,
        context
    ):

        alternative_adjustment = 0.0

        alternative_factors = []

        # Placeholder logic
        # Future:
        # - congressional trading
        # - insider activity
        # - dark pool data
        # - unusual options activity

        politician_bias = "bullish"

        if politician_bias == "bullish":

            alternative_adjustment += 0.03

            alternative_factors.append(
                "Bullish politician trade activity"
            )

        elif politician_bias == "bearish":

            alternative_adjustment -= 0.05

            alternative_factors.append(
                "Bearish politician trade activity"
            )

        return {
            "alternative_adjustment":
                alternative_adjustment,

            "alternative_factors":
                alternative_factors
        }