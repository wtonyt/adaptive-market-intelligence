class ConfidenceEngine:

    def calculate(self, context):

        confidence = 0.0

        reasons = []
        blockers = []

        # Base signal strength
        if context.signal_score >= 0.75:

            confidence += 0.35

            reasons.append(
                "Strong upstream signal score"
            )

        elif context.signal_score >= 0.55:

            confidence += 0.20

            reasons.append(
                "Moderate upstream signal score"
            )

        else:

            blockers.append(
                "Signal score too weak"
            )

        # Volume confirmation
        if context.volume_ratio is not None:

            if context.volume_ratio >= 2.0:

                confidence += 0.25

                reasons.append(
                    "Volume is significantly above normal"
                )

            elif context.volume_ratio >= 1.25:

                confidence += 0.10

                reasons.append(
                    "Volume is moderately elevated"
                )

            else:

                blockers.append(
                    "Volume confirmation is weak"
                )

        # VWAP positioning
        if context.vwap_distance is not None:

            if context.vwap_distance > 0:

                confidence += 0.15

                reasons.append(
                    "Price is above VWAP"
                )

        # Market regime
        if context.market_regime:

            if context.market_regime.lower() in [
                "bullish",
                "momentum",
                "risk_on"
            ]:

                confidence += 0.15

                reasons.append(
                    f"Market regime supports trade: "
                    f"{context.market_regime}"
                )

        confidence = min(
            round(confidence, 2),
            1.0
        )

        return {
            "confidence": confidence,
            "reasons": reasons,
            "blockers": blockers
        }