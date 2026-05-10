# src/api/main.py
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.db.database import Base, engine
from src.services.openclaw_reasoning_engine import reason_over_openclaw_trade
from src.services.trade_events import append_event_log, append_trade_event, event_token_matches


load_dotenv()

app = FastAPI()
security = HTTPBearer()

TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUDIENCE = os.getenv("AZURE_AUDIENCE")
SECRET_KEY = os.getenv("JWT_SECRET", "myjwtsecret")

OPENID_CONFIG = (
    f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"
)

_jwks = None


@app.on_event("startup")
def initialize_database():
    Base.metadata.create_all(bind=engine)


def get_jwks():
    global _jwks
    if _jwks is None:
        config = requests.get(OPENID_CONFIG).json()
        jwks_uri = config["jwks_uri"]
        _jwks = requests.get(jwks_uri).json()
    return _jwks


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if TEST_MODE:
        token = credentials.credentials

        if token == "invalidtoken":
            raise HTTPException(status_code=403, detail="Invalid token")

        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            raise HTTPException(status_code=403, detail="Invalid token")

    try:
        token = credentials.credentials
        jwks = get_jwks()
        headers = jwt.get_unverified_header(token)

        key = next(k for k in jwks["keys"] if k["kid"] == headers["kid"])

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            options={"verify_iss": False},
        )

        issuer = payload.get("iss")
        valid_issuers = [
            f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
            f"https://sts.windows.net/{TENANT_ID}/",
        ]

        if issuer not in valid_issuers:
            raise HTTPException(status_code=403, detail="Invalid issuer")

        return payload

    except Exception as exc:
        raise HTTPException(status_code=403, detail=f"Invalid Azure token: {str(exc)}")


@app.get("/")
def health():
    return {
        "status": "running",
        "default_mode": "openclaw",
        "recommended_ingest": "/events/openclaw/nodeasset-trade",
        "fallback_ingest": "/events/nodeasset-trade",
    }


def _extract_event_token(
    authorization: Optional[str],
    x_event_token: Optional[str],
) -> Optional[str]:
    if x_event_token:
        return x_event_token
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    return authorization


def _verify_event_ingest_token(
    authorization: Optional[str],
    x_event_token: Optional[str],
) -> None:
    provided = _extract_event_token(authorization, x_event_token)
    if not event_token_matches(provided):
        raise HTTPException(status_code=403, detail="Invalid event ingest token")


def _reason_and_record_event(payload: Dict[str, Any], source: str, mode: str):
    _ = append_trade_event(payload, source=source)
    decision = reason_over_openclaw_trade(payload)
    append_event_log(decision["event"])

    return {
        "status": "reasoned",
        "mode": mode,
        "trade_id": decision["event"].get("trade_id"),
        "specialist": decision["event"].get("specialist"),
        "symbol": decision["event"].get("symbol"),
        "decision": decision,
    }


@app.post("/events/openclaw/nodeasset-trade")
def ingest_openclaw_nodeasset_trade(
    payload: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    x_event_token: Optional[str] = Header(None, alias="X-Event-Token"),
):
    _verify_event_ingest_token(authorization, x_event_token)
    return _reason_and_record_event(
        payload,
        source="openclaw_agent",
        mode="openclaw",
    )


@app.post("/events/nodeasset-trade")
def ingest_nodeasset_trade_fallback(
    payload: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    x_event_token: Optional[str] = Header(None, alias="X-Event-Token"),
):
    _verify_event_ingest_token(authorization, x_event_token)
    return _reason_and_record_event(
        payload,
        source="nodeasset_api",
        mode="direct-api-fallback",
    )


@app.post("/run")
def trigger_pipeline(background_tasks: BackgroundTasks, user=Depends(verify_token)):
    print(f"USER PAYLOAD: {user}", flush=True)
    roles = user.get("roles", [])

    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Admin role required")

    from src.pipelines.run_pipeline import run_pipeline

    background_tasks.add_task(run_pipeline)

    return {"status": "pipeline started"}
