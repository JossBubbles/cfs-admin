from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connect import Base


class tecnicojefe(Base):
    __tablename__ = "tecnico_jefe"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    area: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )

    cuenta_usuario: Mapped[Optional["usuario"]] = relationship(
        "usuario",
        back_populates="tecnico_jefe"
    )

    tecnicos_a_cargo: Mapped[List["tecnico"]] = relationship(
        "tecnico",
        back_populates="jefe"
    )
