from src.services.news.regime_performance_tracker import (
    RegimePerformanceTracker
)

tracker = (
    RegimePerformanceTracker()
)

tracker.record_trade(
    "AI_BULLISH_REGIME",
    "WIN"
)

tracker.record_trade(
    "AI_BULLISH_REGIME",
    "WIN"
)

tracker.record_trade(
    "AI_BULLISH_REGIME",
    "LOSS"
)

tracker.record_trade(
    "MACRO_RISK_REGIME",
    "LOSS"
)

summary = (
    tracker.summarize()
)

print(
    "\n--- REGIME PERFORMANCE ---\n"
)

print(summary)