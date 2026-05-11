from src.db.crud_positions import (
    get_open_positions
)


class GovernanceEngine:

    def evaluate(
        self,
        context,
        confidence,
        risk_score
    ):

        blockers = []

        open_positions = (
            get_open_positions()
        )

        # Minimum confidence
        if confidence < 0.70:

            blockers.append(
                "Confidence below threshold"
            )

        # Maximum risk
        if risk_score > 0.40:

            blockers.append(
                "Risk exceeds threshold"
            )

        # Existing position protection
        if context.already_in_position:

            blockers.append(
                "Already in active position"
            )

        # Max open positions
        if len(open_positions) >= 5:

            blockers.append(
                "Maximum open positions reached"
            )

        approved = (
            len(blockers) == 0
        )

        return {
            "approved": approved,
            "blockers": blockers
        }