from src.db.database import SessionLocal

from src.db.models_order import (
    OrderRecord
)


def upsert_order(order_data):

    db = SessionLocal()

    try:

        record = OrderRecord(

            order_id=order_data["order_id"],

            trade_id=order_data["trade_id"],

            symbol=order_data["symbol"],

            status=order_data["status"],

            qty=order_data["qty"],

            filled_qty=order_data["filled_qty"],

            side=order_data["side"]
        )

        db.merge(record)

        db.commit()

        print(
            f"Synced order: "
            f"{record.order_id}"
        )

    finally:

        db.close()