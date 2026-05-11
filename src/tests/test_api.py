import requests

BASE_URL = "http://127.0.0.1:8000"


def test_health():

    r = requests.get(
        f"{BASE_URL}/"
    )

    assert r.status_code == 200


def test_status():

    r = requests.get(
        f"{BASE_URL}/status"
    )

    assert r.status_code == 200

    data = r.json()

    assert data["service"] == "market-ml"


def test_openclaw_analysis():

    payload = {
        "type": "nodeasset.copilot.analysis.requested",
        "user_email": "pytest@example.com",
        "data": {
            "trade_id": "pytest-001",
            "specialist": "runner",
            "symbol": "NVDA",
            "side": "BUY",
            "quantity": 1,
            "price": 100,
            "timestamp": "2026-05-11T00:00:00Z"
        }
    }

    r = requests.post(
        f"{BASE_URL}/events/openclaw/copilot-analysis",
        headers={
            "X-Event-Token": "local-openclaw-token"
        },
        json=payload
    )

    assert r.status_code == 200

    data = r.json()

    assert data["status"] == "ready"

    assert data["mode"] == "openclaw-copilot"