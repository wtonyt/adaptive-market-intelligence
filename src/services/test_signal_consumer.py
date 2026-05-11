from src.services.signal_consumer import process_signal


test_message = {
    "trade_id": "TEST123",
    "action": "BUY",

    "signal": {
        "ticker": "CUE",
        "signal": "MOMENTUM_BREAKOUT",
        "confidence": 0.82,

        "price": 4.25,
        "volume_ratio": 2.6,
        "vwap_distance": 0.04,
        "volatility_score": 0.42,
        "market_regime": "momentum"
    }
}


process_signal(test_message)