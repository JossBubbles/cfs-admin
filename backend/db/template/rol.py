from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connect import Base


class rol(Base):
    __tablename__ = "rol"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True
    )

    usuarios: Mapped[List["usuario"]] = relationship(
        "usuario",
        back_populates="rol"
    )