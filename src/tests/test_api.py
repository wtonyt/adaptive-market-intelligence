import requests
from jose import jwt
import os

BASE_URL = "http://127.0.0.1:8000"

SECRET_KEY = os.getenv("JWT_SECRET", "myjwtsecret")
ALGORITHM = "HS256"


def get_token():
    return jwt.encode({"user": "ci-test"}, SECRET_KEY, algorithm=ALGORITHM)


def test_health():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200


def test_run_success():
    token = get_token()

    r = requests.post(
        f"{BASE_URL}/run",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert r.status_code == 200


def test_run_unauthorized():
    r = requests.post(f"{BASE_URL}/run")
    assert r.status_code == 401

def test_run_invalid_token():
    r = requests.post(
        f"{BASE_URL}/run",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert r.status_code == 403