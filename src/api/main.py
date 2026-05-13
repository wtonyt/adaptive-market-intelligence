import os
import requests

from datetime import datetime, timezone
from threading import Thread

from src.services.poller import (
    poll,
    poll_once,
    NodeAssetClient
)
from fastapi import (
    FastAPI,
    Body,
    Header,
    HTTPException
)

from fastapi.responses import JSONResponse

from src.db.database import (
    Base,
    engine,
    SessionLocal
)

from src.db.models import TradeEvent

from src.config.settings import settings

from src.schemas.copilot_request import (
    CoPilotRequest
)

from src.services.copilot.copilot_analysis_service import (
    CoPilotAnalysisService
)

from src.services.trade_events import (
    append_trade_event,
    update_trade_event_state
)

from src.services.poller import (
    poll_once,
    NodeAssetClient
)
from src.db.crud_copilot_analysis import (
    save_copilot_analysis
)
from src.utils.logger import logger
from src.db.crud_copilot_query import (

    get_recent_copilot_analyses,

    get_copilot_analysis_by_trade_id
)
from src.db.crud_structural_query import (

    get_recent_structural_failures,

    get_failures_by_pattern
)
from src.db.crud_structural_outcome_query import (

    get_recent_structural_outcomes,

    get_structural_outcomes_by_pattern,

    get_structural_pattern_accuracy
)
from src.db.crud_structural_outcome import (
    save_structural_outcome_evaluation
)
from src.services.copilot_analysis_engine import (
    post_analysis_callback
)

app = FastAPI(
    title="Market ML Trading Platform",
    version="1.0.0"
)


Base.metadata.create_all(
    bind=engine
)

@app.on_event("startup")
async def startup_event():

    logger.info(
        "Starting NodeAsset background poller..."
    )

    Thread(
        target=poll,
        daemon=True
    ).start()

@app.get("/")
def health_check():

    logger.info("Health check requested")

    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "timestamp": (
            datetime.now(timezone.utc).isoformat()
        )
    }


@app.get("/status")
def status():

    return {
        "service": "market-ml",
        "environment": settings.ENVIRONMENT,
        "alpaca_paper": settings.ALPACA_PAPER,
        "timestamp": (
            datetime.now(timezone.utc).isoformat()
        )
    }


@app.post("/poll")
def poll_feed():

    logger.info(
        "Manual poll endpoint triggered"
    )

    try:

        client = NodeAssetClient()

        client.login()

        result = poll_once(client)

        return JSONResponse(
            status_code=200,
            content=result
        )

    except Exception as exc:

        logger.error(
            f"Poll endpoint failure: {str(exc)}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(exc)
            }
        )


@app.post("/test-event")
def test_event(
    payload: dict = Body(...)
):

    event = append_trade_event(
        payload,
        source="manual_test"
    )

    return {
        "status": "ingested",
        "event": event
    }


@app.get("/metrics")
def metrics():

    db = SessionLocal()

    try:

        total_events = (
            db.query(TradeEvent)
            .count()
        )

        buy_events = (
            db.query(TradeEvent)
            .filter(
                TradeEvent.side == "BUY"
            )
            .count()
        )

        sell_events = (
            db.query(TradeEvent)
            .filter(
                TradeEvent.side == "SELL"
            )
            .count()
        )

        pending_execution = (
            db.query(TradeEvent)
            .filter(
                TradeEvent.execution_status
                == "NOT_EXECUTED"
            )
            .count()
        )

        return {
            "status": "healthy",
            "total_events": total_events,
            "buy_events": buy_events,
            "sell_events": sell_events,
            "pending_execution": pending_execution
        }

    finally:

        db.close()

@app.get("/copilot/analyses/recent")
def recent_copilot_analyses(
    limit: int = 25
):

    records = (
        get_recent_copilot_analyses(limit)
    )

    return [

        {
            "trade_id": r.trade_id,
            "symbol": r.symbol,
            "user_email": r.user_email,
            "actionability": r.actionability,
            "confidence_score": r.confidence_score,
            "summary": r.summary,
            "callback_sent": r.callback_sent,
            "created_at": r.created_at
        }

        for r in records
    ]

@app.get(
    "/copilot/analysis/{trade_id}"
)
def copilot_analysis_by_trade_id(
    trade_id: str
):

    record = (
        get_copilot_analysis_by_trade_id(
            trade_id
        )
    )

    if not record:

        return {
            "status": "not_found"
        }

    return {

        "trade_id": record.trade_id,

        "symbol": record.symbol,

        "user_email": record.user_email,

        "actionability": record.actionability,

        "confidence_score": (
            record.confidence_score
        ),

        "summary": record.summary,

        "analysis_payload": (
            record.analysis_payload
        ),

        "callback_sent": (
            record.callback_sent
        ),

        "created_at": (
            record.created_at
        )
    }

@app.get(
    "/structural/failures/recent"
)
def recent_structural_failures(
    limit: int = 25
):

    events = (
        get_recent_structural_failures(
            limit
        )
    )

    return [

        {

            "trade_id": e.trade_id,

            "symbol": e.symbol,

            "failure_pattern": (
                e.failure_pattern
            ),

            "severity": e.severity,

            "blocked": e.blocked,

            "reasons": e.reasons,

            "created_at": e.created_at
        }

        for e in events
    ]

@app.get(
    "/structural/failures/{pattern}"
)
def structural_failures_by_pattern(
    pattern: str
):

    events = (
        get_failures_by_pattern(
            pattern
        )
    )

    return [

        {

            "trade_id": e.trade_id,

            "symbol": e.symbol,

            "failure_pattern": (
                e.failure_pattern
            ),

            "severity": e.severity,

            "blocked": e.blocked,

            "reasons": e.reasons,

            "created_at": e.created_at
        }

        for e in events
    ]

@app.get(
    "/structural/outcomes/recent"
)
def recent_structural_outcomes(
    limit: int = 25
):

    outcomes = (
        get_recent_structural_outcomes(
            limit
        )
    )

    return [

        {

            "trade_id": o.trade_id,

            "symbol": o.symbol,

            "failure_pattern": (
                o.failure_pattern
            ),

            "blocked": o.blocked,

            "entry_price": (
                o.entry_price
            ),

            "evaluation_price": (
                o.evaluation_price
            ),

            "pnl_delta_pct": (
                o.pnl_delta_pct
            ),

            "outcome": o.outcome,

            "correct_veto": (
                o.correct_veto
            ),

            "evaluation_notes": (
                o.evaluation_notes
            ),

            "evaluated_at": (
                o.evaluated_at
            )
        }

        for o in outcomes
    ]

@app.get(
    "/structural/outcomes/{pattern}"
)
def structural_outcomes_by_pattern(
    pattern: str
):

    outcomes = (
        get_structural_outcomes_by_pattern(
            pattern
        )
    )

    return [

        {

            "trade_id": o.trade_id,

            "symbol": o.symbol,

            "failure_pattern": (
                o.failure_pattern
            ),

            "blocked": o.blocked,

            "entry_price": (
                o.entry_price
            ),

            "evaluation_price": (
                o.evaluation_price
            ),

            "pnl_delta_pct": (
                o.pnl_delta_pct
            ),

            "outcome": o.outcome,

            "correct_veto": (
                o.correct_veto
            ),

            "evaluation_notes": (
                o.evaluation_notes
            ),

            "evaluated_at": (
                o.evaluated_at
            )
        }

        for o in outcomes
    ]

@app.get(
    "/structural/outcomes/accuracy/{pattern}"
)
def structural_pattern_accuracy(
    pattern: str
):

    return (
        get_structural_pattern_accuracy(
            pattern
        )
    )

@app.post("/test-approve/{trade_id}")
def test_approve(
    trade_id: str
):

    event = update_trade_event_state(
        trade_id=trade_id,
        processing_state="APPROVED",
        execution_status="PENDING"
    )

    if not event:

        return {
            "status": "not_found"
        }

    return {
        "status": "approved",
        "trade_id": trade_id
    }


@app.post("/callback-test")
def callback_test(
    payload: dict = Body(...)
):

    logger.info(
        f"Callback received: {payload}"
    )

    return {
        "status": "callback_received",
        "payload": payload
    }

@app.post(
    "/structural/outcomes/evaluate"
)
def evaluate_structural_outcome(
    payload: dict = Body(...)
):

    evaluation = (
        save_structural_outcome_evaluation(

            trade_id=payload["trade_id"],

            symbol=payload["symbol"],

            failure_pattern=(
                payload["failure_pattern"]
            ),

            blocked=payload["blocked"],

            entry_price=(
                payload["entry_price"]
            ),

            evaluation_price=(
                payload["evaluation_price"]
            ),

            pnl_delta_pct=(
                payload["pnl_delta_pct"]
            ),

            outcome=payload["outcome"],

            correct_veto=(
                payload["correct_veto"]
            ),

            evaluation_notes=(
                payload[
                    "evaluation_notes"
                ]
            )
        )
    )

    return {
        "status": "saved",
        "evaluation_id": evaluation.id
    }

@app.post(
    "/events/openclaw/copilot-analysis"
)
def copilot_analysis(

    payload: CoPilotRequest,

    x_event_token: str = Header(
        default=None
    )
):

    expected_token = os.getenv(
        "EVENT_INGEST_TOKEN",
        "local-openclaw-token"
    )

    if x_event_token != expected_token:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    trade_data = (
        payload.data.model_dump()
    )

    copilot_service = (
        CoPilotAnalysisService()
    )

    analysis = (
        copilot_service.analyze_trade(
            trade_data
        )
    )

    analysis["user_email"] = (
        payload.user_email
    )

    analysis["trade_id"] = (
        trade_data["trade_id"]
    )
    
    callback_sent = False

    try:

        callback_sent = (
            post_analysis_callback(
                analysis
            )
        )

    except Exception as exc:

        logger.error(
            f"Callback failure: {str(exc)}"
        )

    save_copilot_analysis(

        trade_id=trade_data["trade_id"],

        user_email=payload.user_email,

        symbol=trade_data["symbol"],

        actionability=analysis["actionability"],

        confidence_score=analysis["confidence_score"],

        summary=analysis["summary"],

        analysis_payload=analysis,

        callback_url=payload.callback_url,

        callback_sent=callback_sent
    )

    return {
        "status": "ready",
        "mode": "openclaw-copilot",
        "callback_sent": callback_sent,
        "analysis": analysis
    }