from typing import Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from config.load import CONFIG
from config.request import LoginRequest, TokenResponse, RefreshTokenRequest
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from core.deps import get_current_user
from db.controller import get_db
from db.template.user import usuario

router = APIRouter(tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Autentica al usuario contra la base de datos usando Argon2id y emite tokens JWT.
    """
    # 1. Buscar usuario por nombre
    user = db.execute(select(usuario).where(usuario.nombre == data.username)).scalar_one_or_none()

    # 2. Verificar contraseña de forma segura en tiempo constante
    invalid_credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user or not verify_password(data.password, user.contraseña):
        raise invalid_credentials_error

    # 3. Generar tokens JWT
    access_token = create_access_token(subject=user.nombre)
    refresh_token = create_refresh_token(subject=user.nombre)

    return {
        "ok": True,
        "token": access_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshTokenRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Renueva un Access Token a partir de un Refresh Token válido.
    """
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token no válido para renovación.",
            )

        username = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El refresh token ha expirado. Inicie sesión nuevamente.",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token no válido.",
        )

    # Validar existencia del usuario
    user = db.execute(select(usuario).where(usuario.nombre == username)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")

    new_access_token = create_access_token(subject=user.nombre)

    return {
        "ok": True,
        "token": new_access_token,
        "access_token": new_access_token,
        "refresh_token": data.refresh_token,
        "token_type": "bearer",
        "expires_in": CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.get("/me")
def get_current_user_profile(current_user: Annotated[usuario, Depends(get_current_user)]):
    """
    Ruta protegida para verificar la identidad del usuario actual autenticado con Bearer Token.
    """
    return {
        "ok": True,
        "id": current_user.id,
        "nombre": current_user.nombre,
        "direccion": current_user.direccion,
    }