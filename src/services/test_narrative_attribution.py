from src.services.news.narrative_attribution_engine import (
    NarrativeAttributionEngine
)

engine = (
    NarrativeAttributionEngine()
)

engine.attribute_trade(
    "WIN",
    "AI_BULLISH_REGIME"
)

engine.attribute_trade(
    "LOSS",
    "MACRO_RISK_REGIME"
)