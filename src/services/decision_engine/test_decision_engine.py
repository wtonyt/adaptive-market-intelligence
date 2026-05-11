from datetime import datetime

from src.services.decision_engine.models import SignalContext
from src.services.decision_engine.decision_engine import DecisionEngine


context = SignalContext(
    trade_id="TEST123",
    symbol="CUE",
    timestamp=datetime.utcnow(),
    signal_type="MOMENTUM_BREAKOUT",
    signal_score=0.82,
    current_price=4.25,
    volume_ratio=2.6,
    vwap_distance=0.04,
    volatility_score=0.42,
    market_regime="momentum",
    already_in_position=False,
)

engine = DecisionEngine()
decision = engine.evaluate(context)

print(decision.model_dump_json(indent=2))