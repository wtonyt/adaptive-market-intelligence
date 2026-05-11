from src.services.decision_engine.models import (
    SignalContext,
    DecisionResult
)

from src.services.decision_engine.confidence_engine import (
    ConfidenceEngine
)

from src.services.decision_engine.risk_engine import (
    RiskEngine
)

from src.services.decision_engine.governance_engine import (
    GovernanceEngine
)


class DecisionEngine:

    def evaluate(
        self,
        context: SignalContext
    ) -> DecisionResult:

        confidence_engine = (
            ConfidenceEngine()
        )

        risk_engine = (
            RiskEngine()
        )

        governance_engine = (
            GovernanceEngine()
        )

        # Confidence evaluation
        confidence_data = (
            confidence_engine.calculate(
                context
            )
        )

        # Risk evaluation
        risk_data = (
            risk_engine.calculate(
                context
            )
        )

        confidence = confidence_data[
            "confidence"
        ]

        risk_score = risk_data[
            "risk_score"
        ]

        reasons = confidence_data[
            "reasons"
        ]

        blockers = (
            confidence_data[
                "blockers"
            ]
            +
            risk_data[
                "risk_factors"
            ]
        )

        # Governance evaluation
        governance_data = (
            governance_engine.evaluate(
                context,
                confidence,
                risk_score
            )
        )

        approved = governance_data[
            "approved"
        ]

        blockers += governance_data[
            "blockers"
        ]

        action = (
            "ENTER_LONG"
            if approved
            else "NO_TRADE"
        )

        return DecisionResult(

            trade_id=context.trade_id,

            symbol=context.symbol,

            action=action,

            confidence=confidence,

            risk_score=risk_score,

            approved=approved,

            reasons=reasons,

            blockers=blockers,
        )