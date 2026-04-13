# app/models/purchase.py
import enum
from sqlalchemy import String, Integer, Float, ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie


class PurchaseStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class TicketStatus(str, enum.Enum):
    ACTIVE = "active"
    USED = "used"
    CANCELLED = "cancelled"


class Purchase(BaseModel):
    __tablename__ = "purchases"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_info: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[PurchaseStatus] = mapped_column(
        Enum(PurchaseStatus), default=PurchaseStatus.PENDING, nullable=False, index=True
    )

    user: Mapped["User"] = relationship(back_populates="purchases")
    movie: Mapped["Movie"] = relationship(back_populates="purchases")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="purchase", cascade="all, delete-orphan")

    @property
    def is_confirmed(self) -> bool:
        return self.status == PurchaseStatus.CONFIRMED


class Ticket(BaseModel):
    __tablename__ = "tickets"

    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey("purchases.id"), nullable=False, index=True)
    ticket_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    seat_number: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.ACTIVE, nullable=False, index=True
    )

    purchase: Mapped["Purchase"] = relationship(back_populates="tickets")
