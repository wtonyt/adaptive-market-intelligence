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

from src.services.decision_engine.news_intelligence_engine import (
    NewsIntelligenceEngine
)

from src.services.decision_engine.alternative_data_engine import (
    AlternativeDataEngine
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

        news_engine = (
            NewsIntelligenceEngine()
        )

        alternative_engine = (
            AlternativeDataEngine()
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

        # News evaluation
        news_data = (
            news_engine.evaluate(
                context
            )
        )

        # Alternative data evaluation
        alternative_data = (
            alternative_engine.evaluate(
                context
            )
        )

        # Final confidence calculation
        confidence = (

            confidence_data["confidence"]

            + news_data[
                "sentiment_adjustment"
            ]

            + alternative_data[
                "alternative_adjustment"
            ]
        )

        confidence = min(
            round(confidence, 2),
            1.0
        )

        # Risk score
        risk_score = (

            risk_data["risk_score"]

            + news_data[
                "risk_adjustment"
            ]
        )

        risk_score = min(
            round(risk_score, 2),
            1.0
        )

        # Reasons
        reasons = (
            confidence_data["reasons"]

            + news_data["news_factors"]

            + alternative_data[
                "alternative_factors"
            ]
        )

        # Blockers
        blockers = (

            confidence_data["blockers"]

            + risk_data["risk_factors"]
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