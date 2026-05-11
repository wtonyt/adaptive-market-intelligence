import os

from dotenv import load_dotenv


# -----------------------------------
# Load DEV first so ENVIRONMENT exists
# -----------------------------------

load_dotenv(".env.dev")


ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "DEV"
).upper()


# -----------------------------------
# Override with environment-specific file
# -----------------------------------

if ENVIRONMENT == "QA":

    load_dotenv(".env.qa", override=True)

elif ENVIRONMENT == "PROD":

    load_dotenv(".env.prod", override=True)


class Settings:

    ENVIRONMENT = ENVIRONMENT

    POSTGRES_USER = os.getenv(
        "POSTGRES_USER"
    )

    POSTGRES_PASSWORD = os.getenv(
        "POSTGRES_PASSWORD"
    )

    POSTGRES_HOST = os.getenv(
        "POSTGRES_HOST"
    )

    POSTGRES_PORT = os.getenv(
        "POSTGRES_PORT"
    )

    POSTGRES_DB = os.getenv(
        "POSTGRES_DB"
    )

    ALPACA_PAPER = (
        os.getenv(
            "ALPACA_PAPER",
            "true"
        ).lower() == "true"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    POLYGON_API_KEY = os.getenv(
        "POLYGON_API_KEY"
    )

    ALPACA_API_KEY = os.getenv(
        "ALPACA_API_KEY"
    )

    ALPACA_SECRET_KEY = os.getenv(
        "ALPACA_SECRET_KEY"
    )

    TEST_MODE = (
        os.getenv(
            "TEST_MODE",
            "false"
        ).lower() == "true"
    )


settings = Settings()