from collections import Counter

from src.db.database import (
    SessionLocal
)

from src.db.models_narrative_event import (
    NarrativeEventRecord
)


class NarrativeRetrievalEngine:

    def get_recent_summary(
        self,
        limit=50
    ):

        db = SessionLocal()

        try:

            events = (

                db.query(
                    NarrativeEventRecord
                )

                .order_by(
                    NarrativeEventRecord
                    .created_at
                    .desc()
                )

                .limit(limit)

                .all()
            )

            event_types = [

                event.event_type

                for event in events
            ]

            return dict(
                Counter(event_types)
            )

        finally:

            db.close()