from src.db.database import SessionLocal

from src.db.models import (
    CopilotAnalysisRecord
)


def get_recent_copilot_analyses(
    limit: int = 25
):

    db = SessionLocal()

    try:

        records = (

            db.query(
                CopilotAnalysisRecord
            )

            .order_by(
                CopilotAnalysisRecord.created_at.desc()
            )

            .limit(limit)

            .all()
        )

        return records

    finally:

        db.close()


def get_copilot_analysis_by_trade_id(
    trade_id: str
):

    db = SessionLocal()

    try:

        return (

            db.query(
                CopilotAnalysisRecord
            )

            .filter(
                CopilotAnalysisRecord.trade_id
                == trade_id
            )

            .first()
        )

    finally:

        db.close()