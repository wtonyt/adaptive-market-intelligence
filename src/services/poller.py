import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from src.services.trade_events import append_trade_event

load_dotenv()

NODEASSET_API_URL = os.getenv("NODEASSET_API_URL", "https://api.nodeasset.com").rstrip("/")
NODEASSET_LOGIN_PATH = os.getenv("NODEASSET_LOGIN_PATH", "/user/login")
NODEASSET_FEED_PATH = os.getenv("NODEASSET_FEED_PATH", "/gappers/subscribed-trades")
NODEASSET_EMAIL = os.getenv("NODEASSET_EMAIL", "")
NODEASSET_PASSWORD = os.getenv("NODEASSET_PASSWORD", "")
NODEASSET_POLL_SECONDS = float(os.getenv("NODEASSET_POLL_SECONDS", "5"))
NODEASSET_LIMIT = int(os.getenv("NODEASSET_LIMIT", "100"))
NODEASSET_ONCE = os.getenv("NODEASSET_ONCE", "false").lower() == "true"
CURSOR_FILE = Path(os.getenv("NODEASSET_CURSOR_FILE", "data/nodeasset_cursor.txt"))
HTTP_TIMEOUT = float(os.getenv("NODEASSET_HTTP_TIMEOUT", "15"))


class NodeAssetClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.token: Optional[str] = None

    def login(self) -> None:
        if not NODEASSET_EMAIL or not NODEASSET_PASSWORD:
            raise RuntimeError("NODEASSET_EMAIL and NODEASSET_PASSWORD are required")

        response = self.session.post(
            self.url(NODEASSET_LOGIN_PATH),
            json={
                "email": NODEASSET_EMAIL,
                "password": NODEASSET_PASSWORD,
            },
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()

        payload = response.json()
        token = (
            payload.get("token")
            or payload.get("jwt")
            or payload.get("access_token")
            or (payload.get("user") or {}).get("token")
        )

        if not token:
            raise RuntimeError("NodeAsset login succeeded but no token was returned")

        self.token = token

    def subscribed_trades(self, after_id: Optional[str]) -> Dict[str, Any]:
        if not self.token:
            self.login()

        params: Dict[str, Any] = {"limit": NODEASSET_LIMIT}
        if after_id:
            params["after_id"] = after_id

        response = self.session.get(
            self.url(NODEASSET_FEED_PATH),
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=HTTP_TIMEOUT,
        )

        if response.status_code in (401, 403):
            self.login()
            response = self.session.get(
                self.url(NODEASSET_FEED_PATH),
                params=params,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=HTTP_TIMEOUT,
            )

        response.raise_for_status()
        return response.json()

    def url(self, path: str) -> str:
        return f"{NODEASSET_API_URL}/{path.lstrip('/')}"


def load_cursor() -> Optional[str]:
    if not CURSOR_FILE.exists():
        return None

    cursor = CURSOR_FILE.read_text().strip()
    return cursor or None


def save_cursor(cursor: Optional[str]) -> None:
    if not cursor:
        return

    CURSOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_FILE.write_text(cursor)


def poll_once(client: NodeAssetClient) -> Dict[str, Any]:
    cursor = load_cursor()
    payload = client.subscribed_trades(cursor)
    trades: List[Dict[str, Any]] = payload.get("trades") or []

    processed = [append_trade_event(trade, source="nodeasset_api") for trade in trades]
    next_cursor = payload.get("next_cursor")
    save_cursor(next_cursor)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "count": len(processed),
        "next_cursor": next_cursor,
    }
    print(json.dumps(summary), flush=True)
    return summary


def poll() -> None:
    print("NodeAsset subscribed trade poller started", flush=True)
    client = NodeAssetClient()
    client.login()

    while True:
        try:
            poll_once(client)
        except Exception as exc:
            print(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "error",
                "error": str(exc),
            }), flush=True)

            if NODEASSET_ONCE:
                raise

        if NODEASSET_ONCE:
            break

        time.sleep(NODEASSET_POLL_SECONDS)


if __name__ == "__main__":
    poll()
