from src.db.database import SessionLocal

from src.db.models import (
    StructuralFailureEvent
)


def get_recent_structural_failures(
    limit: int = 25
):

    db = SessionLocal()

    try:

        return (

            db.query(
                StructuralFailureEvent
            )

            .order_by(
                StructuralFailureEvent
                .created_at.desc()
            )

            .limit(limit)

            .all()
        )

    finally:

        db.close()


def get_failures_by_pattern(
    failure_pattern: str
):

    db = SessionLocal()

    try:

        return (

            db.query(
                StructuralFailureEvent
            )

            .filter(
                StructuralFailureEvent
                .failure_pattern
                == failure_pattern
            )

            .all()
        )

    finally:

        db.close()