import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import HTTPException


NODEASSET_EVENT_NAME = "nodeasset.trade.received"
EVENT_LOG = Path(os.getenv("NODEASSET_EVENT_LOG", "data/nodeasset_trades.log"))


def unwrap_trade_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(payload.get("data"), dict):
        return payload["data"]
    if isinstance(payload.get("trade"), dict):
        return payload["trade"]
    if isinstance(payload.get("event"), dict):
        return payload["event"]
    return payload


def normalize_trade_event(payload: Dict[str, Any], source: str) -> Dict[str, Any]:
    trade = unwrap_trade_event(payload)
    event_type = payload.get("type") or payload.get("event") or NODEASSET_EVENT_NAME

    if isinstance(event_type, dict):
        event_type = NODEASSET_EVENT_NAME

    return {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "type": event_type,
        "cursor": trade.get("cursor") or trade.get("after_id"),
        "trade_id": trade.get("trade_id") or trade.get("id") or trade.get("_id"),
        "specialist": trade.get("specialist") or trade.get("agent") or trade.get("provider"),
        "symbol": trade.get("symbol") or trade.get("ticker"),
        "side": trade.get("side") or trade.get("action") or trade.get("signal"),
        "quantity": trade.get("quantity") or trade.get("qty"),
        "price": trade.get("price") or trade.get("entry_price") or trade.get("fill_price"),
        "timestamp": trade.get("timestamp") or trade.get("executed_at") or trade.get("created_at"),
        "raw": payload,
    }


def append_trade_event(payload: Dict[str, Any], source: str = "nodeasset_api") -> Dict[str, Any]:
    event = normalize_trade_event(payload, source)

    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True))
        handle.write("\n")

    return event


def event_token_matches(provided: Optional[str]) -> bool:
    expected = os.getenv("EVENT_INGEST_TOKEN", "")
    if not expected:
        return True
    return provided == expected


def validate_event_token(
    expected_token: Optional[str],
    header_token: Optional[str],
    authorization: Optional[str],
):
    if not expected_token:
        return

    bearer_token = None

    if authorization and authorization.lower().startswith("bearer "):
        bearer_token = authorization.split(" ", 1)[1].strip()

    if expected_token not in {header_token, bearer_token}:
        raise HTTPException(
            status_code=403,
            detail="Invalid event ingest token",
        )


def _first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None


def _parse_timestamp(value: Any):
    if not value:
        return datetime.now(timezone.utc)

    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)

    if isinstance(value, str):
        text = value.replace("Z", "+00:00")

        try:
            parsed = datetime.fromisoformat(text)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)

    return datetime.now(timezone.utc)


def _normalize_side(value: Any):
    side = str(value or "").upper()

    if side in {"BUY", "BTO", "LONG"}:
        return "BUY"

    if side in {"SELL", "STC", "SHORT"}:
        return "SELL"

    if side in {"HOLD", "WAIT"}:
        return "HOLD"

    return "HOLD"


def normalize_nodeasset_event(payload: dict):
    envelope = payload or {}
    data = envelope.get("data") or envelope.get("trade") or envelope

    symbol = _first_present(
        data.get("symbol"),
        data.get("ticker"),
        envelope.get("symbol"),
        envelope.get("ticker"),
    )

    specialist = _first_present(
        data.get("specialist"),
        data.get("agent"),
        data.get("source"),
        envelope.get("specialist"),
        envelope.get("agent"),
        "nodeasset",
    )

    trade_id = _first_present(
        data.get("trade_id"),
        data.get("id"),
        data.get("_id"),
        envelope.get("trade_id"),
        envelope.get("id"),
    )

    raw_side = _first_present(
        data.get("side"),
        data.get("action"),
        data.get("signal"),
        data.get("direction"),
        envelope.get("side"),
        envelope.get("action"),
    )

    confidence = _first_present(
        data.get("confidence"),
        data.get("score"),
        envelope.get("confidence"),
    )

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = float(os.getenv("NODEASSET_DEFAULT_CONFIDENCE", "0.82"))

    price = _first_present(
        data.get("price"),
        data.get("entry_price"),
        data.get("fill_price"),
        data.get("mark"),
        envelope.get("price"),
    )

    try:
        price = float(price) if price is not None else None
    except (TypeError, ValueError):
        price = None

    event_timestamp = _first_present(
        data.get("timestamp"),
        data.get("created_at"),
        data.get("trade_date"),
        envelope.get("timestamp"),
    )

    event_type = envelope.get("event") or envelope.get("type") or NODEASSET_EVENT_NAME

    if event_type != NODEASSET_EVENT_NAME:
        event_type = NODEASSET_EVENT_NAME

    if not symbol:
        raise HTTPException(
            status_code=422,
            detail="NodeAsset trade event must include symbol or ticker",
        )

    return {
        "event": event_type,
        "trade_id": str(trade_id) if trade_id is not None else None,
        "symbol": str(symbol).upper(),
        "side": _normalize_side(raw_side),
        "specialist": str(specialist).lower(),
        "confidence": max(0.0, min(confidence, 1.0)),
        "price": price,
        "timestamp": _parse_timestamp(event_timestamp),
        "liquidity_score": _first_present(
            data.get("liquidity_score"),
            envelope.get("liquidity_score"),
        ),
        "timing_score": _first_present(
            data.get("timing_score"),
            envelope.get("timing_score"),
        ),
        "raw": envelope,
    }


def append_event_log(event: dict):
    log_path = os.getenv("NODEASSET_REASONED_EVENT_LOG")

    if not log_path:
        return

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = event.get("timestamp")

    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()

    serializable = {
        **event,
        "timestamp": timestamp,
    }

    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(serializable, sort_keys=True))
        handle.write("\n")
