import logging

from src.config.settings import settings


logging.basicConfig(
    level=getattr(
        logging,
        settings.LOG_LEVEL.upper(),
        logging.INFO
    ),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)


logger = logging.getLogger("market_ml")

if __name__ == "__main__":

    logger.debug("Debug logging enabled")

    logger.info("Info logging enabled")

    logger.warning("Warning logging enabled")