from src.services.news.narrative_intelligence_service import (
    NarrativeIntelligenceService
)

service = (
    NarrativeIntelligenceService()
)

service.process_event({
    "event_type": "AI_THEME"
})

service.process_event({
    "event_type": "AI_THEME"
})

service.process_event({
    "event_type": "AI_THEME"
})

service.process_event({
    "event_type": "AI_THEME"
})

regime = (
    service.get_current_regime()
)

print(
    "\n--- CURRENT NARRATIVE REGIME ---\n"
)

print(regime)