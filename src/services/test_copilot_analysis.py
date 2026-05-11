from datetime import datetime

from src.services.copilot.copilot_analysis_service import (
    CoPilotAnalysisService
)

service = (
    CoPilotAnalysisService()
)

trade_data = {

    "trade_id": "trd_001",

    "specialist": "runner",

    "symbol": "NVDA",

    "side": "BUY",

    "quantity": 10,

    "price": 915.25,

    "timestamp": datetime.utcnow()
}

analysis = (
    service.analyze_trade(
        trade_data
    )
)

print(
    "\n--- COPILOT ANALYSIS ---\n"
)

print(
    analysis
)