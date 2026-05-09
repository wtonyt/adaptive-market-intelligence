import time

from src.db.database import SessionLocal
from src.db.models import SignalEvent


def replay_events(delay_seconds: float = 1.0):
    db = SessionLocal()

    try:
        events = (
            db.query(SignalEvent)
            .order_by(SignalEvent.timestamp.asc())
            .all()
        )

        print(f"Loaded {len(events)} events for replay", flush=True)

        for event in events:
            replay_payload = {
                "id": event.id,
                "timestamp": event.timestamp.isoformat() if event.timestamp else None,
                "signal": {
                    "ticker": event.ticker,
                    "signal": event.signal,
                    "confidence": event.confidence,
                },
                "action": event.action,
                "position": event.position,
            }

            print("\n--- REPLAY EVENT ---", flush=True)
            print(replay_payload, flush=True)

            time.sleep(delay_seconds)

    finally:
        db.close()


if __name__ == "__main__":
    replay_events()