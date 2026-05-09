import os
import json
from src.db.crud import save_signal_event
from src.schemas.events import SignalEvent
from azure.servicebus import ServiceBusClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE")


def process_signal(message_data):

    signal = message_data.get("signal", {})
    action = message_data.get("action")

    print("\n--- DECISION ENGINE ---", flush=True)
    print(f"Ticker: {signal.get('ticker')}", flush=True)
    print(f"Signal: {signal.get('signal')}", flush=True)
    print(f"Confidence: {signal.get('confidence')}", flush=True)
    print(f"Action: {action}", flush=True)

    save_signal_event(message_data)

    # Future ML inference goes HERE


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