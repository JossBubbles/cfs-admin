import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from config.load import CONFIG

# Hasher seguro basado en Argon2id
pwd_context = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Genera el hash seguro de una contraseña usando Argon2id."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash en tiempo constante."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_jwt_token(data: dict, expires_delta: timedelta, token_type: str = "access") -> str:
    """
    Crea un token JWT firmado criptográficamente.
    Incluye claims requeridos: sub, iat, exp y type.
    """
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
    """Genera un Access Token de corta duración."""
    data = {"sub": str(subject)}
    if extra_claims:
        data.update(extra_claims)
    return create_jwt_token(
        data=data,
        expires_delta=timedelta(minutes=CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: str | int) -> str:
    """Genera un Refresh Token de mayor duración."""
    data = {"sub": str(subject)}
    return create_jwt_token(
        data=data,
        expires_delta=timedelta(days=CONFIG.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str) -> dict:
    """
    Decodifica y valida la firma y expiración de un JWT.
    Lanza excepciones de PyJWT si es inválido o expiró.
    """
    return jwt.decode(
        token,
        CONFIG.JWT_SECRET_KEY,
        algorithms=[CONFIG.JWT_ALGORITHM],
        options={"require": ["exp", "iat", "sub"]},
    )
