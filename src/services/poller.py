import time
import random
from datetime import datetime, timezone
import json

print("Poller script loaded", flush=True)

current_position = None  # None or "LONG"
entry_price = None

# -----------------------------
# Mock Signal Generator
# -----------------------------
def get_mock_signal():
    return {
        "ticker": "AAPL",
        "signal": random.choice(["BUY", "SELL", "HOLD"]),
        "confidence": round(random.uniform(0.5, 0.95), 2)
    }


# -----------------------------
# Decision Engine (rules-based)
# -----------------------------
def decide(signal):
    global current_position, entry_price

    action = "NO_ACTION"

    if current_position is None:
        # Only allow BUY if not already in a position
        if signal["signal"] == "BUY" and signal["confidence"] > 0.7:
            action = "ENTER_LONG"
            current_position = "LONG"
            entry_price = 100  # placeholder for now

    elif current_position == "LONG":
        # Only allow SELL if in a position
        if signal["signal"] == "SELL" and signal["confidence"] > 0.7:
            action = "EXIT_LONG"
            current_position = None
            entry_price = None

    return action


# -----------------------------
# Main Poll Loop
# -----------------------------
def poll():
    print("Poller started...", flush=True)

    while True:
        print("Polling...", flush=True)

        try:
            signal = get_mock_signal()
            action = decide(signal)

            output = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "signal": signal,
                "action": action,
                "position": current_position
                        }

            # ✅ Console log
            print(output, flush=True)

            # ✅ NEW: Save to file
            with open("decisions.log", "a") as f:
                f.write(json.dumps(output) + "\n")

        except Exception as e:
            print({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "error",
                "error": str(e)
            }, flush=True)

        time.sleep(10)


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    poll()