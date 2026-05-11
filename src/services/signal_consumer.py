import os
import json

from azure.servicebus import ServiceBusClient
from dotenv import load_dotenv

from src.db.crud import save_signal_event
from src.schemas.events import SignalEvent
from src.db.crud_decision import save_decision_result
from src.services.decision_engine.context_builder import (
    build_signal_context
)

from src.services.decision_engine.decision_engine import (
    DecisionEngine
)

load_dotenv()

CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE")


def process_signal(message_data):

    signal = message_data.get("signal", {})
    action = message_data.get("action")

    # Build intelligence context
    context = build_signal_context(message_data)

    # Run decision engine
    engine = DecisionEngine()

    decision = engine.evaluate(context)

    print("\n--- INTELLIGENCE LAYER ---", flush=True)

    print(f"Ticker: {decision.symbol}", flush=True)
    print(f"Action: {decision.action}", flush=True)
    print(f"Approved: {decision.approved}", flush=True)
    print(f"Confidence: {decision.confidence}", flush=True)
    print(f"Risk: {decision.risk_score}", flush=True)

    print(f"Reasons: {decision.reasons}", flush=True)
    print(f"Blockers: {decision.blockers}", flush=True)

    # Persist original signal event
    save_signal_event(message_data)
    save_decision_result(decision)
    # Future:
    # save_decision_result(decision)
    # execute_trade(decision)
    # trigger_gpt_reasoning(decision)


def consume_messages():

    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STRING
    )

    with servicebus_client:

        receiver = servicebus_client.get_queue_receiver(
            queue_name=QUEUE_NAME,
            max_wait_time=5
        )

        with receiver:

            print("Decision Engine listening...", flush=True)

            while True:

                messages = receiver.receive_messages(
                    max_message_count=10,
                    max_wait_time=5
                )

                for message in messages:

                    try:

                        raw_body = b"".join(
                            [b for b in message.body]
                        ).decode("utf-8")

                        data = json.loads(raw_body)

                        event = SignalEvent(**data)

                        process_signal(event.model_dump())

                        receiver.complete_message(message)

                    except Exception as e:

                        print(
                            f"Error processing message: {e}",
                            flush=True
                        )


if __name__ == "__main__":
    consume_messages()