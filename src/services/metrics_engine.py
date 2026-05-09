from collections import Counter

from sqlalchemy import func

from src.db.database import SessionLocal
from src.db.models import SignalEvent


def generate_metrics():

    db = SessionLocal()

    try:

        total_events = db.query(SignalEvent).count()

        avg_confidence = (
            db.query(func.avg(SignalEvent.confidence))
            .scalar()
        )

        actions = (
            db.query(SignalEvent.action)
            .all()
        )

        signals = (
            db.query(SignalEvent.signal)
            .all()
        )

        action_counts = Counter(
            [a[0] for a in actions]
        )

        signal_counts = Counter(
            [s[0] for s in signals]
        )

        print("\n===== STRATEGY METRICS =====", flush=True)

        print(f"Total Events: {total_events}", flush=True)

        print(
            f"Average Confidence: "
            f"{round(avg_confidence or 0, 4)}",
            flush=True
        )

        print("\nAction Distribution:", flush=True)

        for action, count in action_counts.items():
            print(f"  {action}: {count}", flush=True)

        print("\nSignal Distribution:", flush=True)

        for signal, count in signal_counts.items():
            print(f"  {signal}: {count}", flush=True)

    finally:
        db.close()


if __name__ == "__main__":
    generate_metrics()