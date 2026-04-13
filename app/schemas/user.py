# app/schemas/user.py
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class UserProfileResponse(BaseModel):
    id: int
    email: str
    phone: str
    first_name: str
    last_name: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_orm(cls, u):
        return cls(
            id=u.id, email=u.email, phone=u.phone,
            first_name=u.first_name, last_name=u.last_name,
            full_name=u.full_name, role=u.role.value,
            is_active=u.is_active, created_at=u.created_at,
        )


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)


# ── Purchases ──────────────────────────────────────────────────────────────────

class TicketResponse(BaseModel):
    id: int
    ticket_code: str
    seat_number: str
    status: str
    created_at: datetime

    @classmethod
    def from_orm(cls, t):
        return cls(
            id=t.id,
            ticket_code=t.ticket_code,
            seat_number=t.seat_number,
            status=t.status.value if hasattr(t.status, "value") else t.status,
            created_at=t.created_at,
        )


class PurchaseMovieInfo(BaseModel):
    id: int
    title: str
    genre: str
    duration: int
    poster_url: str


class MyPurchaseResponse(BaseModel):
    id: int
    movie_id: int
    movie: Optional[PurchaseMovieInfo]
    quantity: int
    total_amount: float
    status: str
    tickets: List[TicketResponse]
    created_at: datetime

    @classmethod
    def from_orm(cls, p):
        movie_info = None
        if p.movie:
            movie_info = PurchaseMovieInfo(
                id=p.movie.id,
                title=p.movie.title,
                genre=p.movie.genre,
                duration=p.movie.duration,
                poster_url=p.movie.poster_url,
            )
        return cls(
            id=p.id,
            movie_id=p.movie_id,
            movie=movie_info,
            quantity=p.quantity,
            total_amount=p.total_amount,
            status=p.status.value if hasattr(p.status, "value") else p.status,
            tickets=[TicketResponse.from_orm(t) for t in p.tickets],
            created_at=p.created_at,
        )
