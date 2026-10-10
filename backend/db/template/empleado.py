from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.connect import Base


class empleado(Base):
    __tablename__ = "empleado"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    usuario: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    contraseña: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )