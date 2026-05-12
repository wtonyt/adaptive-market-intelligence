import os
import requests

from datetime import datetime, timezone

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

from src.utils.logger import logger


app = FastAPI(
    title="Market ML Trading Platform",
    version="1.0.0"
)


Base.metadata.create_all(
    bind=engine
)


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

    callback_sent = False

    if payload.callback_url:

        try:

            requests.post(

                payload.callback_url,

                json={
                    "status": "completed",
                    "analysis": analysis
                },

                timeout=10
            )

            callback_sent = True

        except Exception as exc:

            logger.error(
                f"Callback failure: {str(exc)}"
            )

    return {
        "status": "ready",
        "mode": "openclaw-copilot",
        "callback_sent": callback_sent,
        "analysis": analysis
    }