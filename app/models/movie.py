# app/models/movie.py — minimal: solo columnas que existen en cinema_booking.movies
# booking-service crea la tabla con: title, genre, duration, rating, price,
# available_tickets, max_capacity, poster_url (+ BaseModel: id, created_at, updated_at, is_active)
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float

from .base import BaseModel

if TYPE_CHECKING:
    from .purchase import Purchase


class Movie(BaseModel):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[str] = mapped_column(String(10), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    available_tickets: Mapped[int] = mapped_column(Integer, nullable=True)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    poster_url: Mapped[str] = mapped_column(String(1000), nullable=True)

    purchases: Mapped[List["Purchase"]] = relationship(back_populates="movie")
