import time

from datetime import datetime

from src.schemas.intelligence_event import (
    IntelligenceEvent
)

from src.services.intelligence_router import (
    IntelligenceRouter
)


class IntelligenceRuntime:

    def __init__(self):

        self.router = (
            IntelligenceRouter()
        )

    def start(self):

        print(
            "\nStarting Intelligence Runtime..."
        )

        while True:

            try:

                # Simulated heartbeat event

                event = IntelligenceEvent(

                    event_type="SYSTEM_EVENT",

                    symbol=None,

                    source="runtime",

                    timestamp=datetime.utcnow(),

                    payload={
                        "heartbeat": True
                    }
                )

                self.router.route(
                    event
                )

                time.sleep(10)

            except Exception as e:

                print(
                    f"\nRuntime Error: {e}"
                )