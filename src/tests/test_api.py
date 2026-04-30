import requests
import os

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY", "supersecret123")


def test_health():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200


def test_run_success():
    r = requests.post(
        f"{BASE_URL}/run",
        headers={"x-api-key": API_KEY}
    )
    assert r.status_code == 200


def test_run_unauthorized():
    r = requests.post(f"{BASE_URL}/run")
    assert r.status_code == 401