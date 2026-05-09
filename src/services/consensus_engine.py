from datetime import datetime, timezone
from src.db.crud import save_consensus_event
from src.schemas.signals import (
    TraderSignal,
    ConsensusSignal
)
from src.services.agent_weight_engine import (
    calculate_dynamic_weights
)

LIQUIDITY_WEIGHT = 0.20
TIMING_WEIGHT = 0.20

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

    weights = calculate_dynamic_weights()

    ml_weight = weights.get(
        "ML",
        0.5
    )

    rl_weight = weights.get(
        "RL",
        0.5
    )
    consensus = (
        ml_signal.side == rl_signal.side
    )

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

    weighted_agent_confidence = (
        (ml_signal.confidence * ml_weight)
        +
        (rl_signal.confidence * rl_weight)
    )

    market_context_score = (
        (avg_liquidity * LIQUIDITY_WEIGHT)
        +
        (avg_timing * TIMING_WEIGHT)
    )

    confidence_score = (
        weighted_agent_confidence
        +
        market_context_score
    )

    confidence_score = min(
        confidence_score,
        1.0
    )

    if not consensus:
        confidence_score *= 0.50    

    print(
        f"Dynamic Weights → "
        f"ML={round(ml_weight, 4)} "
        f"RL={round(rl_weight, 4)}",
        flush=True
    )
    
    # -----------------------------------
    # Final Decision
    # -----------------------------------

    if consensus and confidence_score >= 0.85:

        final_side = ml_signal.side

        reason = (
            "High-confidence consensus"
        )

    elif consensus and confidence_score >= 0.70:

        final_side = "HOLD"

        reason = (
            "Moderate-confidence consensus"
        )

    else:

        final_side = "SKIP"

        reason = (
            "Low-confidence or disagreement"
        )

    return ConsensusSignal(

        symbol=ml_signal.symbol,

        ml_side=ml_signal.side,

        rl_side=rl_signal.side,

        consensus=consensus,

        consensus_score=(
            1.0 if consensus else 0.0
        ),

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