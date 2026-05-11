from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

from src.config.settings import settings


if settings.TEST_MODE:

    DATABASE_URL = (
        "sqlite:///./test.db"
    )

else:

    DATABASE_URL = (
        f"postgresql://"
        f"{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )


engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }
    if settings.TEST_MODE
    else {}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()