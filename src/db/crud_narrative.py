import uuid

from src.db.database import (
    SessionLocal
)

from src.db.models_narrative_event import (
    NarrativeEventRecord
)


def save_narrative_event(
    narrative_event
):

    db = SessionLocal()

    try:

        record = NarrativeEventRecord(

            id=str(uuid.uuid4()),

            event_type=narrative_event.get(
                "event_type"
            ),

            sentiment=narrative_event.get(
                "sentiment"
            ),

            symbol=narrative_event.get(
                "symbol"
            ),

            source=narrative_event.get(
                "source"
            ),

            payload=narrative_event
        )

        db.add(record)

        db.commit()

        print(
            "Saved narrative event"
        )

    finally:

        db.close()