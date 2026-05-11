from src.db.database import SessionLocal
from src.db.models_decision import DecisionRecord


def save_decision_result(decision):

    db = SessionLocal()

    try:

        record = DecisionRecord(
            trade_id=decision.trade_id,
            symbol=decision.symbol,
            action=decision.action,
            confidence=decision.confidence,
            risk_score=decision.risk_score,
            approved=decision.approved,
            reasons=decision.reasons,
            blockers=decision.blockers
        )

        db.merge(record)

        db.commit()

        print("Saved decision record", flush=True)

    finally:

        db.close()