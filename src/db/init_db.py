from src.db.database import engine, Base
from src.db.models_position import *
from src.db.models import *
from src.db.models_decision import *
from src.db.models_trade_outcome import *
from src.utils.logger import logger
from src.db.models_order import *


def init_db():

    logger.info(
        "Creating database tables"
    )

    print(engine.url)

    print(Base.metadata.tables.keys())

    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database initialization complete"
    )


if __name__ == "__main__":

    init_db()