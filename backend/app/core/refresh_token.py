import secrets
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_db
from app.models.refresh_token import RefreshToken


def create_refresh_token_string() -> str:
    return secrets.token_urlsafe(64)


def get_refresh_token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)


async def store_refresh_token(db: AsyncSession, user_id: uuid.UUID, token: str) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=get_refresh_token_expiry(),
    )
    db.add(refresh_token)
    await db.flush()
    return refresh_token


async def validate_refresh_token(db: AsyncSession, token: str) -> uuid.UUID:
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.expires_at > datetime.now(UTC),
        )
    )
    refresh_token = result.scalar_one_or_none()

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    await db.delete(refresh_token)
    await db.flush()

    return refresh_token.user_id


async def invalidate_all_user_tokens(db: AsyncSession, user_id: uuid.UUID) -> None:
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    tokens = result.scalars().all()
    for token in tokens:
        await db.delete(token)
    await db.flush()
