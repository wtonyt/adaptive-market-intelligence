from src.services.news.narrative_retrieval_engine import (
    NarrativeRetrievalEngine
)

engine = (
    NarrativeRetrievalEngine()
)

summary = (
    engine.get_recent_summary()
)

print(
    "\n--- RETRIEVED NARRATIVE SUMMARY ---\n"
)

print(summary)