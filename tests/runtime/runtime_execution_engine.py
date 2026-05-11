from datetime import datetime

from src.services.decision_engine.models import (
    DecisionResult
)

from src.services.execution.alpaca_executor import (
    AlpacaExecutor
)


decision = DecisionResult(

    trade_id="EXEC001",

    symbol="AAPL",

    action="ENTER_LONG",

    confidence=0.90,

    risk_score=0.10,

    approved=True,

    reasons=["Test execution"],

    blockers=[]
)


executor = AlpacaExecutor()

executor.execute_trade(
    decision
)