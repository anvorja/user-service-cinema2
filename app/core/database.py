# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── cinema_booking (read-only: purchases, tickets) ────────────────────────────

def _make_booking_engine():
    url = settings.BOOKING_DATABASE_URL
    if not url:
        return None
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=2,
        max_overflow=3,
        pool_timeout=30,
        echo=settings.DEBUG,
    )


_booking_engine = _make_booking_engine()
BookingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_booking_engine) if _booking_engine else None


def get_booking_db():
    if BookingSessionLocal is None:
        from fastapi import HTTPException, status
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Booking DB no configurada")
    db = BookingSessionLocal()
    try:
        yield db
    finally:
        db.close()
