from src.services.decision_engine.models import (
    SignalContext
)


def build_signal_context(
    data
):

    return SignalContext(

        trade_id=data.get(
            "trade_id"
        ),

        symbol=data.get(
            "symbol"
        ),

        signal_type=data.get(
            "signal_type"
        ),

        timestamp=data.get(
            "timestamp"
        ),

        current_price=data.get(
            "current_price"
        ),

        signal_score=data.get(
            "signal_score",
            0.0
        ),

        market_regime=data.get(
            "market_regime"
        ),

        volume_ratio=data.get(
            "volume_ratio"
        ),

        volatility_score=data.get(
            "volatility_score"
        ),

        vwap_distance=data.get(
            "vwap_distance"
        ),

        already_in_position=data.get(
            "already_in_position",
            False
        )
    )