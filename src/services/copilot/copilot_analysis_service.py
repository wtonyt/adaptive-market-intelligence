from src.services.decision_engine.models import (
    SignalContext
)

from src.services.decision_engine.decision_engine import (
    DecisionEngine
)

from src.services.news.narrative_intelligence_service import (
    NarrativeIntelligenceService
)

from src.services.filters.structural_failure_filter import (
    StructuralFailureFilter
)
from src.db.crud_structural_failure import (
    save_structural_failure_event
)

class CoPilotAnalysisService:

    def __init__(self):

        self.engine = (
            DecisionEngine()
        )

        self.narrative_service = (
            NarrativeIntelligenceService()
        )

        self.structural_filter = (
            StructuralFailureFilter()
        )

    def analyze_trade(
        self,
        trade_data
    ):

        context = SignalContext(

            trade_id=trade_data[
                "trade_id"
            ],

            symbol=trade_data[
                "symbol"
            ],

            signal_type=trade_data[
                "side"
            ],

            timestamp=trade_data[
                "timestamp"
            ],

            current_price=trade_data[
                "price"
            ],

            signal_score=0.80,

            market_regime="momentum",

            volume_ratio=1.8,

            volatility_score=0.35,

            vwap_distance=0.10,

            already_in_position=False
        )

        decision = (
            self.engine.evaluate(
                context
            )
        )

        narrative_regime = (
            self.narrative_service
            .get_current_regime()
        )

        structural_analysis = (
            self.structural_filter.evaluate(
                trade_data
            )
        )

        actionability = (
            "strong_watch"
            if decision.confidence >= 0.85
            else "watch"
        )

        summary = (
            f"{trade_data['side']} "
            f"signal on "
            f"{trade_data['symbol']} "
            f"is classified as "
            f"{actionability}. "
            f"Narrative regime is "
            f"{narrative_regime}."
        )

        reasons = list(
            decision.reasons
        )

        risks = list(
            decision.blockers
        )

        # -----------------------------------
        # Structural failure override
        # -----------------------------------

        if structural_analysis["blocked"]:

            actionability = "avoid"

            reasons.extend(
                structural_analysis[
                    "reasons"
                ]
            )

            risks.append(
                structural_analysis[
                    "failure_pattern"
                ]
            )

            summary += (
                " Structural failure "
                "patterns detected."
            )

            save_structural_failure_event(

                trade_id=trade_data[
                    "trade_id"
                ],

                symbol=trade_data[
                    "symbol"
                ],

                failure_pattern=(
                    structural_analysis[
                        "failure_pattern"
                    ]
                ),

                severity=(
                    structural_analysis[
                        "severity"
                    ]
                ),

                blocked=(
                    structural_analysis[
                        "blocked"
                    ]
                ),

                reasons=(
                    structural_analysis[
                        "reasons"
                    ]
                ),

                raw_context=trade_data
            )
        
        questions = [

            "Is the trade still near the original entry price?",

            "Has volume remained elevated since signal generation?",

            "Does current market momentum still support the setup?"
        ]

        return {

            "trade_id":
                trade_data[
                    "trade_id"
                ],

            "actionability":
                actionability,

            "summary":
                summary,

            "confidence_score":
                decision.confidence,

            "reasons":
                reasons,

            "risks":
                risks,

            "questions":
                questions,

            "structural_analysis":
                structural_analysis
        }