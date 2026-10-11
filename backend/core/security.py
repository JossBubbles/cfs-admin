import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from config.load import CONFIG

# Hasher seguro basado en Argon2id
pwd_context = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_jwt_token(data: dict, expires_delta: timedelta, token_type: str = "access") -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    to_encode.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": token_type,
    })

    return jwt.encode(to_encode, CONFIG.JWT_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM)


def create_access_token(subject: str | int, extra_claims: dict | None = None) -> str:
    data = {"sub": str(subject)}
    if extra_claims:
        data.update(extra_claims)
    return create_jwt_token(
        data=data,
        expires_delta=timedelta(minutes=CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: str | int) -> str:
    data = {"sub": str(subject)}
    return create_jwt_token(
        data=data,
        expires_delta=timedelta(days=CONFIG.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        CONFIG.JWT_SECRET_KEY,
        algorithms=[CONFIG.JWT_ALGORITHM],
        options={"require": ["exp", "iat", "sub"]},
    )
