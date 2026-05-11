class RiskEngine:

    def calculate(self, context):

        risk_score = 0.10

        risk_factors = []

        if context.volatility_score:

            if context.volatility_score > 0.80:

                risk_score += 0.30

                risk_factors.append(
                    "Extremely high volatility"
                )

            elif context.volatility_score > 0.60:

                risk_score += 0.15

                risk_factors.append(
                    "Elevated volatility"
                )

        if context.vwap_distance is not None:

            if context.vwap_distance < 0:

                risk_score += 0.15

                risk_factors.append(
                    "Trading below VWAP"
                )

        if context.volume_ratio:

            if context.volume_ratio < 1.0:

                risk_score += 0.10

                risk_factors.append(
                    "Weak relative volume"
                )

        risk_score = min(
            round(risk_score, 2),
            1.0
        )

        return {
            "risk_score": risk_score,
            "risk_factors": risk_factors
        }