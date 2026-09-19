from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from configs.settings import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        password_hash,
    )


def create_access_token(
    user_id: int,
    project_id: int,
    role: str,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes,
    )

    payload = {
        "sub": str(user_id),
        "project_id": project_id,
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(
    user_id: int,
    project_id: int,
    role: str,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days,
    )

    payload = {
        "sub": str(user_id),
        "project_id": project_id,
        "role": role,
        "type": "refresh",
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_refresh_token(
    refresh_token: str,
) -> dict:
    payload = jwt.decode(
        refresh_token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token.")

    return payload
