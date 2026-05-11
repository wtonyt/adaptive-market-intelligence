from src.services.decision_engine.news_intelligence_engine import (
    NewsIntelligenceEngine
)

from src.services.decision_engine.trade_management_engine import (
    TradeManagementEngine
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

            # Future:
            # decision evaluation

        elif event.event_type == "ORDER_EVENT":

            print(
                "Routing to Execution Layer"
            )

        elif event.event_type == "RISK_EVENT":

            print(
                "Routing to Governance Layer"
            )

        else:

            print(
                "Unknown event type"
            )

        print(
            "Event routed successfully"
        )