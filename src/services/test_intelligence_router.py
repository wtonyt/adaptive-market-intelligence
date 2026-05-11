from datetime import datetime

from src.schemas.intelligence_event import (
    IntelligenceEvent
)

from src.services.intelligence_router import (
    IntelligenceRouter
)

router = IntelligenceRouter()

events = [

    IntelligenceEvent(
        event_type="NEWS_EVENT",
        symbol="AAPL",
        source="alpaca_news",
        timestamp=datetime.utcnow(),
        payload={
            "symbol": "AAPL"
        }
    ),

    IntelligenceEvent(
        event_type="POSITION_EVENT",
        symbol="AAPL",
        source="alpaca",
        timestamp=datetime.utcnow(),
        payload={}
    ),

    IntelligenceEvent(
        event_type="RISK_EVENT",
        symbol="SPY",
        source="governance_engine",
        timestamp=datetime.utcnow(),
        payload={}
    )
]

for event in events:

    router.route(event)