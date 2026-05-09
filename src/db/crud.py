from src.db.database import SessionLocal
from src.db.models import SignalEvent


def save_signal_event(data: dict):

    db = SessionLocal()

    try:

        signal = data.get("signal", {})

        event = SignalEvent(
            ticker=signal.get("ticker"),
            signal=signal.get("signal"),
            confidence=signal.get("confidence"),
            action=data.get("action"),
            position=data.get("position"),
            timestamp=data.get("timestamp")
        )

        db.add(event)
        db.commit()

        print("Saved event to PostgreSQL", flush=True)

    finally:
        db.close()