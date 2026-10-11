from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connect import Base


class tecnico(Base):
    __tablename__ = "tecnico"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    especialidad: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )

    jefe_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tecnico_jefe.id", ondelete="SET NULL"),
        nullable=True
    )

    cuenta_usuario: Mapped[Optional["usuario"]] = relationship(
        "usuario",
        back_populates="tecnico"
    )

    jefe: Mapped[Optional["tecnicojefe"]] = relationship(
        "tecnicojefe",
        back_populates="tecnicos_a_cargo"
    )