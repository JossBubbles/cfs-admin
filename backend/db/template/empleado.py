from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connect import Base


class empleado(Base):
    __tablename__ = "empleado"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    cargo: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    telefono: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )

    cuenta_usuario: Mapped[Optional["usuario"]] = relationship(
        "usuario",
        back_populates="empleado"
    )