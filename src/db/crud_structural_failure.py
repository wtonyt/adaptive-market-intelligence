from src.db.database import SessionLocal

from src.db.models import (
    StructuralFailureEvent
)


def save_structural_failure_event(

    trade_id: str,

    symbol: str,

    failure_pattern: str,

    severity: float,

    blocked: bool,

    reasons: list,

    raw_context: dict
):

    db = SessionLocal()

    try:

        event = StructuralFailureEvent(

            trade_id=trade_id,

            symbol=symbol,

            failure_pattern=failure_pattern,

            severity=severity,

            blocked=blocked,

            reasons=reasons,

            raw_context=raw_context
        )

        db.add(event)

        db.commit()

        db.refresh(event)

        return event

    finally:

        db.close()