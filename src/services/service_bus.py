import os
import json

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE")


def publish_signal(signal_data: dict):

    if not CONNECTION_STRING:
        raise Exception("Missing SERVICE_BUS_CONNECTION_STRING")

    if not QUEUE_NAME:
        raise Exception("Missing SERVICE_BUS_QUEUE")

    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STRING
    )

    with servicebus_client:

        sender = servicebus_client.get_queue_sender(
            queue_name=QUEUE_NAME
        )

        with sender:

            message = ServiceBusMessage(
                json.dumps(signal_data)
            )

            sender.send_messages(message)

            print(
                f"Published message to queue '{QUEUE_NAME}'",
                flush=True
            )