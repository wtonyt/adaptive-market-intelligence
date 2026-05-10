import os
from datetime import datetime, timezone

from src.db.crud import save_consensus_event, save_signal_event
from src.schemas.signals import ConsensusSignal, TraderSignal
from src.services.market_regime_engine import detect_market_regime
from src.services.position_sizing_engine import calculate_position_size
from src.services.trade_events import normalize_nodeasset_event


def _score(value, default):
    try:
        return max(0.0, min(float(value), 1.0))
    except (TypeError, ValueError):
        return default


def nodeasset_event_to_signal(event: dict):
    liquidity_default = float(os.getenv("NODEASSET_DEFAULT_LIQUIDITY_SCORE", "0.75"))
    timing_default = float(os.getenv("NODEASSET_DEFAULT_TIMING_SCORE", "0.75"))

    return TraderSignal(
        source=f"NodeAsset:{event['specialist']}",
        symbol=event["symbol"],
        side=event["side"],
        confidence=event["confidence"],
        timestamp=event["timestamp"],
        suggested_price=event["price"],
        liquidity_score=_score(event.get("liquidity_score"), liquidity_default),
        timing_score=_score(event.get("timing_score"), timing_default),
        metadata={
            "trade_id": event.get("trade_id"),
            "specialist": event["specialist"],
            "event": event["event"]
        }
    )


def reason_over_openclaw_trade(payload: dict):
    event = normalize_nodeasset_event(payload)
    signal = nodeasset_event_to_signal(event)
    regime = detect_market_regime(signal.symbol)

    market_context_score = (
        ((signal.liquidity_score or 0)
        +
        (signal.timing_score or 0))
        / 2
    )

    confidence_score = min(
        1.0,
        round((signal.confidence * 0.70) + (market_context_score * 0.30), 4)
    )

    threshold = float(os.getenv("NODEASSET_OPENCLAW_ACTION_THRESHOLD", "0.70"))

    if signal.side == "HOLD":
        final_side = "HOLD"
        reason = "OpenClaw held the NodeAsset specialist signal for review"
    elif confidence_score >= threshold:
        final_side = signal.side
        reason = (
            "OpenClaw accepted the NodeAsset specialist signal after "
            "confidence, liquidity, timing, and regime checks"
        )
    else:
        final_side = "SKIP"
        reason = (
            "OpenClaw skipped the NodeAsset specialist signal because "
            "confidence did not clear the configured threshold"
        )

    position_percent = calculate_position_size(
        confidence_score,
        regime
    )

    consensus = ConsensusSignal(
        symbol=signal.symbol,
        ml_side=None,
        rl_side=signal.side,
        consensus=final_side in {"BUY", "SELL"},
        consensus_score=confidence_score,
        final_side=final_side,
        confidence_score=confidence_score,
        reason=reason,
        timestamp=datetime.now(timezone.utc)
    )

    save_signal_event({
        "signal": {
            "ticker": signal.symbol,
            "signal": signal.side,
            "confidence": signal.confidence
        },
        "action": final_side,
        "position": str({
            "position_percent": position_percent,
            "suggested_price": signal.suggested_price,
            "regime": regime,
            "source": signal.source
        }),
        "timestamp": signal.timestamp
    })

    save_consensus_event(consensus)

    return {
        "event": {
            **event,
            "timestamp": event["timestamp"].isoformat()
        },
        "signal": signal.model_dump(mode="json"),
        "reasoning": {
            "mode": "openclaw",
            "regime": regime,
            "threshold": threshold,
            "position_percent": position_percent,
            "market_context_score": round(market_context_score, 4),
            "notes": [
                "NodeAsset is treated as the subscribed specialist signal.",
                "OpenClaw applies the local reasoning layer before producing an action.",
                "Direct NodeAsset API handoff remains a fallback integration path."
            ]
        },
        "consensus": consensus.model_dump(mode="json"),
        "recommended_action": final_side
    }
