# app/api/routes.py
from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db, get_booking_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.purchase import Purchase
from app.models.movie import Movie
from app.schemas.user import UserProfileResponse, UserUpdate, MyPurchaseResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Perfil del usuario autenticado (datos en cinema_users)."""
    return UserProfileResponse.from_orm(current_user)


@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualizar nombre, apellido o teléfono."""
    updated = UserService.update_profile(db, current_user.id, data)
    return UserProfileResponse.from_orm(updated)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Soft-delete en cinema_users + publica user.deactivated →
    auth-service desactiva en cinema_auth para bloquear futuros logins.
    """
    await UserService.delete_account(db, current_user.id)


@router.get("/me/purchases", response_model=List[MyPurchaseResponse])
async def get_my_purchases(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    purchase_status: str = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    booking_db: Session = Depends(get_booking_db),
):
    """Historial de compras del usuario autenticado (lee cinema_booking)."""
    q = (
        booking_db.query(Purchase)
        .options(
            selectinload(Purchase.tickets),
            selectinload(Purchase.movie),
        )
        .filter(Purchase.user_id == current_user.id)
    )
    if purchase_status:
        q = q.filter(Purchase.status == purchase_status)
    purchases = q.order_by(Purchase.id.desc()).offset(skip).limit(limit).all()
    return [MyPurchaseResponse.from_orm(p) for p in purchases]
