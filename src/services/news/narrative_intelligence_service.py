from src.services.news.narrative_memory import (
    NarrativeMemory
)

from src.services.news.narrative_regime_engine import (
    NarrativeRegimeEngine
)

from src.services.news.narrative_retrieval_engine import (
    NarrativeRetrievalEngine
)

from src.db.crud_narrative import (
    save_narrative_event
)


class NarrativeIntelligenceService:

    def __init__(self):

        self.memory = (
            NarrativeMemory()
        )

        self.regime_engine = (
            NarrativeRegimeEngine()
        )

        self.retrieval_engine = (
            NarrativeRetrievalEngine()
        )

    def process_event(
        self,
        classified_event
    ):

        # Runtime memory
        self.memory.store_event(
            classified_event
        )

        # Persistent memory
        save_narrative_event(
            classified_event
        )

    def get_current_regime(self):

        summary = (
            self.retrieval_engine
            .get_recent_summary()
        )

        regime = (
            self.regime_engine
            .detect_regime(
                summary
            )
        )

        return regime