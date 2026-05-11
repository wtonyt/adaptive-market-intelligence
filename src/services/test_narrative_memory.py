from src.services.news.narrative_memory import (
    NarrativeMemory
)

memory = NarrativeMemory()

memory.store_event({
    "event_type": "AI_THEME"
})

memory.store_event({
    "event_type": "AI_THEME"
})

memory.store_event({
    "event_type": "BUFFETT_THEME"
})

summary = memory.summarize()

print("\n--- NARRATIVE MEMORY ---\n")

print(summary)