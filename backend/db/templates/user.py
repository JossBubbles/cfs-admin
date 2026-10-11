from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connect import Base


class usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    contraseña: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    direccion: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True
    )

    rol_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("rol.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relaciones
    rol: Mapped[Optional["rol"]] = relationship(
        "rol",
        back_populates="usuarios"
    )

    empleado: Mapped[Optional["empleado"]] = relationship(
        "empleado",
        back_populates="cuenta_usuario",
        uselist=False
    )

    tecnico: Mapped[Optional["tecnico"]] = relationship(
        "tecnico",
        back_populates="cuenta_usuario",
        uselist=False
    )

    tecnico_jefe: Mapped[Optional["tecnicojefe"]] = relationship(
        "tecnicojefe",
        back_populates="cuenta_usuario",
        uselist=False
    )