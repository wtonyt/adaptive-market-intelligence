from datetime import datetime

from src.schemas.intelligence_event import IntelligenceEvent


event = IntelligenceEvent(
    event_type="NEWS_EVENT",
    symbol="AAPL",
    source="alpaca_news",
    timestamp=datetime.utcnow(),
    payload={
        "headline": "Apple surges after bullish AI outlook",
        "sentiment": "BULLISH",
        "confidence_adjustment": 0.05,
        "risk_adjustment": 0.0
    }
)

print(event.model_dump_json(indent=2))