from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.security import decode_token
from db.controller import get_db
from db.template.user import usuario

# Esquema Bearer estándar de FastAPI
security_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> usuario:
    """
    Valida el token Bearer recibido en la cabecera Authorization y retorna el usuario autenticado.
    Lanza 401 si el token no es válido, expiró o no corresponde a un Access Token.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación no válidas o expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        token_type: str = payload.get("type")
        username: str = payload.get("sub")

        # Asegurar que no se pueda usar un Refresh Token para acceder a endpoints
        if token_type != "access" or username is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de acceso ha expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    # Buscar usuario en la base de datos
    user = db.execute(select(usuario).where(usuario.nombre == username)).scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
