from sqlalchemy import (
    Column,
    String,
    Integer,
    Float
)

from src.db.database import Base


class RegimePerformanceRecord(Base):

    __tablename__ = (
        "regime_performance"
    )

    regime = Column(
        String,
        primary_key=True
    )

    wins = Column(
        Integer,
        default=0
    )

    losses = Column(
        Integer,
        default=0
    )

    win_rate = Column(
        Float,
        default=0.0
    )