import os
from datetime import datetime, timezone
from typing import Any, Dict

import requests

from src.services.openclaw_reasoning_engine import reason_over_openclaw_trade


def _trade_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    return data or {}


def build_copilot_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:
    trade = _trade_from_payload(payload)
    user_email = payload.get("user_email") or trade.get("user_email")
    trade_id = trade.get("trade_id") or trade.get("id")

    decision = reason_over_openclaw_trade({
        "event": "nodeasset.trade.received",
        "user_email": user_email,
        "data": trade,
    })

    action = decision["recommended_action"]
    confidence = decision["consensus"]["confidence_score"]
    reasoning = decision["reasoning"]
    signal = decision["signal"]

    if action in {"BUY", "SELL"} and confidence >= 0.82:
        actionability = "actionable"
    elif action in {"BUY", "SELL"}:
        actionability = "strong_watch"
    elif action == "HOLD":
        actionability = "watch"
    else:
        actionability = "avoid"

    symbol = signal["symbol"]
    specialist = trade.get("specialist") or signal.get("metadata", {}).get("specialist")
    side = signal["side"]
    price = signal.get("suggested_price")

    reasons = [
        f"{specialist} issued a {side} signal on {symbol}.",
        f"Composite confidence is {confidence}.",
        f"Market regime is {reasoning['regime']}.",
        f"Suggested position size is {reasoning['position_percent']}.",
    ]

    risks = []
    if reasoning["regime"] == "UNKNOWN":
        risks.append("Market regime is unknown because the local candle store does not yet have enough symbol history.")
    if actionability in {"avoid", "watch"}:
        risks.append("The signal did not clear the action threshold for an immediate action recommendation.")
    if not price:
        risks.append("The event did not include a usable signal price.")

    summary = (
        f"{specialist} {side} on {symbol} is classified as {actionability}. "
        f"The review is decision support for a human trader, not an autonomous execution instruction."
    )

    return {
        "user_email": user_email,
        "trade_id": trade_id,
        "status": "ready",
        "actionability": actionability,
        "summary": summary,
        "confidence_score": confidence,
        "reasons": reasons,
        "risks": risks,
        "questions": [
            "Is this signal still close to the original price?",
            "How does this compare to recent trades from the same specialist?",
            "What would make this setup stale?",
        ],
        "market_context": {
            "regime": reasoning["regime"],
            "market_context_score": reasoning["market_context_score"],
            "position_percent": reasoning["position_percent"],
        },
        "similar_trades": [],
        "raw_reasoning": decision,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def post_analysis_callback(analysis: Dict[str, Any]) -> bool:
    url = os.getenv("NODEASSET_COPILOT_RESULT_URL", "").strip()
    if not url:
        return False

    headers = {"Content-Type": "application/json"}
    token = os.getenv("NODEASSET_COPILOT_RESULT_TOKEN", "").strip()
    if token:
        headers["X-Event-Token"] = token

    response = requests.post(
        url,
        json={
            "user_email": analysis.get("user_email"),
            "trade_id": analysis.get("trade_id"),
            "analysis": analysis,
        },
        headers=headers,
        timeout=float(os.getenv("NODEASSET_COPILOT_CALLBACK_TIMEOUT", "8")),
    )
    response.raise_for_status()
    return True


def answer_copilot_question(payload: Dict[str, Any]) -> str:
    message = (payload.get("message") or "").strip()
    analysis = payload.get("analysis") or {}
    summary = analysis.get("summary") or "This trade has not been fully analyzed yet."
    reasons = " ".join((analysis.get("reasons") or [])[:3])
    risks = " ".join((analysis.get("risks") or [])[:2])

    return (
        f"{summary} For your question, '{message}', the current review points to: "
        f"{reasons or 'no supporting reasons saved yet.'} "
        f"{('Risks: ' + risks) if risks else ''}"
    ).strip()
