from src.db.database import engine
from src.db.models import Base

from src.utils.logger import logger


def init_db():

    logger.info(
        "Creating database tables"
    )

    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database initialization complete"
    )


if __name__ == "__main__":

    init_db()