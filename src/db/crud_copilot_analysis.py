from uuid import uuid4

from src.db.database import SessionLocal

from src.db.models import (
    CopilotAnalysisRecord
)


def save_copilot_analysis(

    trade_id: str,

    user_email: str,

    symbol: str,

    actionability: str,

    confidence_score: float,

    summary: str,

    analysis_payload: dict,

    callback_url: str = None,

    callback_sent: bool = False
):

    db = SessionLocal()

    try:

        record = CopilotAnalysisRecord(

            id=str(uuid4()),

            trade_id=trade_id,

            user_email=user_email,

            symbol=symbol,

            actionability=actionability,

            confidence_score=confidence_score,

            summary=summary,

            analysis_payload=analysis_payload,

            callback_url=callback_url,

            callback_sent=callback_sent
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        return record

    finally:

        db.close()