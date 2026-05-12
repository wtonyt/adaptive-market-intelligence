from src.db.database import SessionLocal

from src.db.models import (
    StructuralOutcomeEvaluation
)


def save_structural_outcome_evaluation(

    trade_id: str,

    symbol: str,

    failure_pattern: str,

    blocked: bool,

    entry_price: float,

    evaluation_price: float,

    pnl_delta_pct: float,

    outcome: str,

    correct_veto: bool,

    evaluation_notes: str
):

    db = SessionLocal()

    try:

        evaluation = (
            StructuralOutcomeEvaluation(

                trade_id=trade_id,

                symbol=symbol,

                failure_pattern=(
                    failure_pattern
                ),

                blocked=blocked,

                entry_price=entry_price,

                evaluation_price=(
                    evaluation_price
                ),

                pnl_delta_pct=(
                    pnl_delta_pct
                ),

                outcome=outcome,

                correct_veto=(
                    correct_veto
                ),

                evaluation_notes=(
                    evaluation_notes
                )
            )
        )

        db.add(evaluation)

        db.commit()

        db.refresh(evaluation)

        return evaluation

    finally:

        db.close()