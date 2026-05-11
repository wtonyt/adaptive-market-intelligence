from src.db.database import SessionLocal
from src.db.models_position import ActivePosition


def get_open_positions():
    db = SessionLocal()

    try:
        return db.query(ActivePosition).filter(
            ActivePosition.open == True
        ).all()

    finally:
        db.close()


def upsert_active_position(position_data):
    db = SessionLocal()

    try:
        record = ActivePosition(
            trade_id=position_data["trade_id"],
            symbol=position_data["symbol"],
            side=position_data["side"],
            entry_price=position_data["entry_price"],
            quantity=position_data["quantity"],
            exposure=position_data["exposure"],
            open=position_data["open"],
        )

        db.merge(record)
        db.commit()

        print(
            f"Synced active position: {record.symbol}",
            flush=True
        )

    finally:
        db.close()