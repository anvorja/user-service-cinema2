# app/services/user_service.py
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdate

logger = logging.getLogger(__name__)


class UserService:

    @staticmethod
    def get_profile(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
        return user

    @staticmethod
    def update_profile(db: Session, user_id: int, data: UserUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    async def delete_account(db: Session, user_id: int) -> None:
        """
        Soft-delete en cinema_users + publica user.deactivated para que
        auth-service invalide el acceso en cinema_auth.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")

        user.is_active = False
        db.commit()

        try:
            from app.kafka.producer import publish_event
            await publish_event("user.deactivated", {"user_id": user_id})
        except Exception as e:
            logger.warning("Could not publish user.deactivated: %s", e)
