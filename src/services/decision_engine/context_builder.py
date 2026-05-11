from datetime import datetime

from src.services.decision_engine.models import SignalContext


def build_signal_context(message_data):

    signal = message_data.get("signal", {})

    return SignalContext(
        trade_id=message_data.get("trade_id", "UNKNOWN"),
        symbol=signal.get("ticker"),
        timestamp=datetime.utcnow(),

        signal_type=signal.get("signal"),
        signal_score=signal.get("confidence", 0.0),

        current_price=signal.get("price", 0.0),

        volume_ratio=signal.get("volume_ratio"),
        vwap_distance=signal.get("vwap_distance"),
        volatility_score=signal.get("volatility_score"),
        market_regime=signal.get("market_regime"),

        already_in_position=False
    )