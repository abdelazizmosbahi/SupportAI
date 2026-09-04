import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.refresh_token import (
    create_refresh_token_string,
    invalidate_all_user_tokens,
    store_refresh_token,
    validate_refresh_token,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    existing = await db.execute(select(User).where(User.email == user_data.email))
    if existing.scalar_one_or_none():
        raise ValueError("Email already registered")

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, login_data: LoginRequest) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(login_data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User is inactive")

    access_token = create_access_token(user.id)
    refresh_token_string = create_refresh_token_string()
    await store_refresh_token(db, user.id, refresh_token_string)
    user_response = UserResponse.model_validate(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_string,
        user=user_response,
    )


async def refresh_access_token(db: AsyncSession, refresh_data: RefreshRequest) -> TokenResponse:
    user_id = await validate_refresh_token(db, refresh_data.refresh_token)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise ValueError("User not found or inactive")

    access_token = create_access_token(user.id)
    refresh_token_string = create_refresh_token_string()
    await store_refresh_token(db, user.id, refresh_token_string)
    user_response = UserResponse.model_validate(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_string,
        user=user_response,
    )


async def logout_user(db: AsyncSession, user_id: uuid.UUID) -> None:
    await invalidate_all_user_tokens(db, user_id)
