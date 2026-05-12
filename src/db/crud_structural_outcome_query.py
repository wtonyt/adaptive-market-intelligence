from src.db.database import SessionLocal

from src.db.models import (
    StructuralOutcomeEvaluation
)


def get_recent_structural_outcomes(
    limit: int = 25
):

    db = SessionLocal()

    try:

        return (

            db.query(
                StructuralOutcomeEvaluation
            )

            .order_by(
                StructuralOutcomeEvaluation
                .evaluated_at.desc()
            )

            .limit(limit)

            .all()
        )

    finally:

        db.close()


def get_structural_outcomes_by_pattern(
    failure_pattern: str
):

    db = SessionLocal()

    try:

        return (

            db.query(
                StructuralOutcomeEvaluation
            )

            .filter(
                StructuralOutcomeEvaluation
                .failure_pattern == failure_pattern
            )

            .all()
        )

    finally:

        db.close()


def get_structural_pattern_accuracy(
    failure_pattern: str
):

    db = SessionLocal()

    try:

        records = (

            db.query(
                StructuralOutcomeEvaluation
            )

            .filter(
                StructuralOutcomeEvaluation
                .failure_pattern == failure_pattern
            )

            .all()
        )

        total = len(records)

        if total == 0:

            return {
                "failure_pattern": failure_pattern,
                "total": 0,
                "correct_vetoes": 0,
                "accuracy": 0
            }

        correct = sum(
            1 for r in records
            if r.correct_veto
        )

        return {
            "failure_pattern": failure_pattern,
            "total": total,
            "correct_vetoes": correct,
            "accuracy": round(
                correct / total,
                4
            )
        }

    finally:

        db.close()