from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.connect import Base


class rol(Base):
    __tablename__ = "rol"

    nombre: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )