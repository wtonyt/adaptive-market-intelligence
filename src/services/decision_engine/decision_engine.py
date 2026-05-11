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
from src.services.news.narrative_intelligence_service import (
    NarrativeIntelligenceService
)
from src.services.news.shared_regime_tracker import (
    shared_regime_tracker
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

        narrative_service = (
            NarrativeIntelligenceService()
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

        # Narrative regime
        narrative_regime = (
            narrative_service
            .get_current_regime()
        )

        performance_summary = (
            shared_regime_tracker
            .summarize()
        )

        regime_stats = (
            performance_summary.get(
                narrative_regime,
                {}
            )
        )

        regime_win_rate = (
            regime_stats.get(
                "win_rate",
                0
            )
        )

        # Base confidence
        confidence = (

            confidence_data["confidence"]

            + news_data[
                "sentiment_adjustment"
            ]

            + alternative_data[
                "alternative_adjustment"
            ]
        )

        # Base risk
        risk_score = (

            risk_data["risk_score"]

            + news_data[
                "risk_adjustment"
            ]
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

        # Narrative regime adjustments
        if narrative_regime == "AI_BULLISH_REGIME":

            confidence += 0.05

            reasons.append(
                "AI bullish narrative regime detected"
            )

        elif narrative_regime == (
            "LEADERSHIP_CONFIDENCE_REGIME"
        ):

            confidence += 0.03

            reasons.append(
                "Leadership confidence regime detected"
            )

        elif narrative_regime == (
            "VALUE_CONFIDENCE_REGIME"
        ):

            confidence += 0.02

            reasons.append(
                "Value confidence regime detected"
            )
            
        elif narrative_regime == "MACRO_RISK_REGIME":

            confidence -= 0.05

            risk_score += 0.10

            blockers.append(
                "Macro risk narrative regime detected"
            )

        # Experience-weighted adjustments

        if regime_win_rate >= 0.75:

            confidence += 0.03

            reasons.append(
                "Historical regime performance is strong"
            )

        elif (
            regime_win_rate > 0
            and regime_win_rate <= 0.40
        ):

            confidence -= 0.05

            risk_score += 0.05

            blockers.append(
                "Historical regime performance is weak"
            )
        # Normalize
        confidence = min(
            round(confidence, 2),
            1.0
        )

        risk_score = min(
            round(risk_score, 2),
            1.0
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