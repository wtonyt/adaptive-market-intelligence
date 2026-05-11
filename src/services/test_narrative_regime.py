from src.services.news.narrative_regime_engine import (
    NarrativeRegimeEngine
)

engine = (
    NarrativeRegimeEngine()
)

summary = {

    "AI_THEME": 4,

    "BUFFETT_THEME": 1
}

regime = (
    engine.detect_regime(
        summary
    )
)

print(
    "\n--- NARRATIVE REGIME ---\n"
)

print(regime)