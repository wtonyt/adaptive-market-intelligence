from datetime import datetime, timezone
from src.db.crud import save_consensus_event
from src.schemas.signals import (
    TraderSignal,
    ConsensusSignal
)


# -----------------------------------
# Mock ML Signal
# -----------------------------------

def mock_ml_signal():

    return TraderSignal(
        source="ML",

        symbol="AAPL",

        side="BUY",

        confidence=0.82,

        timestamp=datetime.now(timezone.utc),

        liquidity_score=0.90,

        timing_score=0.75
    )


# -----------------------------------
# Mock RL Signal
# -----------------------------------

def mock_rl_signal():

    return TraderSignal(
        source="RL",

        symbol="AAPL",

        side="BUY",

        confidence=0.78,

        timestamp=datetime.now(timezone.utc),

        liquidity_score=0.88,

        timing_score=0.80
    )


# -----------------------------------
# Consensus Logic
# -----------------------------------

def build_consensus(
    ml_signal: TraderSignal,
    rl_signal: TraderSignal
):

    consensus = (
        ml_signal.side == rl_signal.side
    )

    avg_confidence = (
        ml_signal.confidence
        + rl_signal.confidence
    ) / 2

    avg_liquidity = (
        (ml_signal.liquidity_score or 0)
        +
        (rl_signal.liquidity_score or 0)
    ) / 2

    avg_timing = (
        (ml_signal.timing_score or 0)
        +
        (rl_signal.timing_score or 0)
    ) / 2

    confidence_score = (
        avg_confidence * 0.5
        +
        avg_liquidity * 0.25
        +
        avg_timing * 0.25
    )

    # -----------------------------------
    # Final Decision
    # -----------------------------------

    if consensus and confidence_score > 0.75:

        final_side = ml_signal.side

        reason = (
            "ML and RL agree with "
            "high confidence"
        )

    elif consensus:

        final_side = "HOLD"

        reason = (
            "Consensus exists but "
            "confidence is moderate"
        )

    else:

        final_side = "SKIP"

        reason = (
            "ML and RL disagree"
        )

    return ConsensusSignal(

        symbol=ml_signal.symbol,

        ml_side=ml_signal.side,

        rl_side=rl_signal.side,

        consensus=consensus,

        consensus_score=1.0 if consensus else 0.0,

        final_side=final_side,

        confidence_score=round(
            confidence_score,
            4
        ),

        reason=reason,

        timestamp=datetime.now(timezone.utc)
    )


# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    ml_signal = mock_ml_signal()

    rl_signal = mock_rl_signal()

    result = build_consensus(
        ml_signal,
        rl_signal
    )

    print("\n===== CONSENSUS RESULT =====\n")

    print(
        result.model_dump(
            mode="json"
        )
    )

    save_consensus_event(result)