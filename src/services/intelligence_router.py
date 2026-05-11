from src.config.settings import settings
from src.services.decision_engine.news_intelligence_engine import (
    NewsIntelligenceEngine
)

from src.services.decision_engine.trade_management_engine import (
    TradeManagementEngine
)

from src.services.decision_engine.context_builder import (
    build_signal_context
)

from src.services.decision_engine.decision_engine import (
    DecisionEngine
)

from src.services.execution.alpaca_executor import (
    AlpacaExecutor
)

class IntelligenceRouter:

    def __init__(self):

        self.news_engine = (
            NewsIntelligenceEngine()
        )

        self.trade_manager = (
            TradeManagementEngine()
        )

    def route(
        self,
        event
    ):

        print(
            "\n--- ROUTING EVENT ---"
        )

        print(
            f"Type: "
            f"{event.event_type}"
        )

        if event.event_type == "NEWS_EVENT":

            print(
                "Routing to News Intelligence"
            )

            result = (
                self.news_engine.evaluate(
                    event.payload
                )
            )

            print(
                "\n--- NEWS ANALYSIS ---"
            )

            print(result)

            # Future:
            # evaluate narrative impact

        elif event.event_type == "POSITION_EVENT":

            print(
                "Routing to Trade Manager"
            )

            # Future:
            # evaluate exit logic

        elif event.event_type == "SIGNAL_EVENT":

            print(
                "Routing to Decision Engine"
            )

            print(
                "\nSignal Payload:"
            )

            print(
                event.payload
            )

            context = (
                build_signal_context(
                    event.payload
                )
            )

            engine = (
                DecisionEngine()
            )

            decision = (
                engine.evaluate(
                    context
                )
            )

            print(
                "\n--- LIVE DECISION ---"
            )

            print(
                f"Symbol: {decision.symbol}"
            )

            print(
                f"Action: {decision.action}"
            )

            print(
                f"Confidence: "
                f"{decision.confidence}"
            )

            print(
                f"Risk: "
                f"{decision.risk_score}"
            )

            print(
                f"Approved: "
                f"{decision.approved}"
            )

            print(
                f"Reasons: "
                f"{decision.reasons}"
            )

            print(
                f"Blockers: "
                f"{decision.blockers}"
            )

            if decision.approved and not settings.TEST_MODE:

                print(
                    "\nRouting approved trade "
                    "to execution engine..."
                )

                execution_engine = (
                    AlpacaExecutor()
                )

                execution_engine.execute_trade(
                    decision
                )