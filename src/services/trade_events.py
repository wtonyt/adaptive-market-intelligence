import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


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
    event_type = payload.get("type") or "nodeasset.trade.received"

    return {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "type": event_type,
        "cursor": trade.get("cursor") or trade.get("after_id"),
        "trade_id": trade.get("trade_id") or trade.get("id"),
        "specialist": trade.get("specialist") or trade.get("agent") or trade.get("provider"),
        "symbol": trade.get("symbol"),
        "side": trade.get("side") or trade.get("action"),
        "quantity": trade.get("quantity") or trade.get("qty"),
        "price": trade.get("price") or trade.get("entry_price"),
        "timestamp": trade.get("timestamp") or trade.get("executed_at"),
        "raw": payload,
    }


def append_trade_event(payload: Dict[str, Any], source: str = "nodeasset_api") -> Dict[str, Any]:
    event = normalize_trade_event(payload, source)

    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")

    return event


def event_token_matches(provided: Optional[str]) -> bool:
    expected = os.getenv("EVENT_INGEST_TOKEN", "")
    if not expected:
        return True
    return provided == expected
