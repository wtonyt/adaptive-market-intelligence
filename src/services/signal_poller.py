import time

from datetime import datetime

from src.schemas.intelligence_event import (
    IntelligenceEvent
)

from src.services.intelligence_router import (
    IntelligenceRouter
)


class SignalPoller:

    def __init__(self):

        self.router = (
            IntelligenceRouter()
        )

    def start(self):

        print(
            "\nStarting Signal Poller..."
        )

        while True:

            try:

                # Simulated live signal

                signal_payload = {

                    "trade_id": "LIVE_SIGNAL_001",

                    "symbol": "CUE",

                    "signal_type": "MOMENTUM_LONG",

                    "timestamp": datetime.utcnow(),

                    "current_price": 4.82,

                    "signal_score": 0.91,

                    "market_regime": "momentum",

                    "volume_ratio": 2.4,

                    "volatility_score": 0.35,

                    "vwap_distance": 0.12,

                    "already_in_position": False
                }

                event = IntelligenceEvent(

                    event_type="SIGNAL_EVENT",

                    symbol="CUE",

                    source="signal_engine",

                    timestamp=datetime.utcnow(),

                    payload=signal_payload
                )

                self.router.route(
                    event
                )

                time.sleep(20)

            except Exception as e:

                print(
                    f"\nSignal Poller Error: {e}"
                )