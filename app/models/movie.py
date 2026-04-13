# app/models/movie.py — minimal: only needed for purchase.movie relation
import enum
from datetime import date
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, Date, Enum

from .base import BaseModel

if TYPE_CHECKING:
    from .purchase import Purchase


class MovieStatus(str, enum.Enum):
    IN_THEATERS = "in_theaters"
    COMING_SOON = "coming_soon"
    ENDED = "ended"


class Movie(BaseModel):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    director: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[MovieStatus] = mapped_column(Enum(MovieStatus), nullable=False)
    is_presale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    available_tickets: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    backdrop_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    detail_1_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    detail_2_url: Mapped[str] = mapped_column(String(1000), nullable=False)

    purchases: Mapped[List["Purchase"]] = relationship(back_populates="movie")
