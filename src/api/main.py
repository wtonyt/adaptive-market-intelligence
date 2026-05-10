from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.services.poller import poll_once, NodeAssetClient
from src.utils.logger import logger


app = FastAPI(
    title="Market ML Trading Platform",
    version="1.0.0"
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