class StructuralFailureFilter:

    def evaluate(
        self,
        trade_context: dict
    ):

        avg_liq = (
            trade_context.get("avg_liq")
            or 0
        )

        min_liq = (
            trade_context.get("min_liq")
            or 0
        )

        avg_bad_p = (
            trade_context.get("avg_bad_p")
            or 0
        )

        float_size = (
            trade_context.get("float_size")
            or 0
        )

        reasons = []

        blocked = False

        severity = 0.0

        # -----------------------------------
        # Liquidity dumping hypothesis
        # -----------------------------------

        if avg_liq > 3000 and min_liq <= 200:

            blocked = True

            severity += 0.45

            reasons.append(
                "Liquidity structure suggests "
                "possible seller pressure."
            )

        # -----------------------------------
        # Weak trade quality pattern
        # -----------------------------------

        if avg_bad_p >= 0.20:

            severity += 0.20

            reasons.append(
                "Historical bad trade probability "
                "is elevated."
            )

        # -----------------------------------
        # Float instability
        # -----------------------------------

        if float_size < 1000000:

            severity += 0.15

            reasons.append(
                "Low float may create unstable "
                "price behavior."
            )

        # -----------------------------------
        # Final classification
        # -----------------------------------

        failure_pattern = None

        if blocked:

            failure_pattern = (
                "HIGH_LIQUIDITY_DUMPING_RISK"
            )

        return {

            "blocked": blocked,

            "severity": round(
                severity,
                2
            ),

            "failure_pattern": (
                failure_pattern
            ),

            "reasons": reasons
        }