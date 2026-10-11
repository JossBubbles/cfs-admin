import sys
from typing import Generator
from config.load import CONFIG

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from db.connect import Base


URL_DB = (
    f"postgresql+psycopg://{CONFIG.POSTGRES_USER}:{CONFIG.POSTGRES_PASSWORD}@{CONFIG.POSTGRES_HOST}:"
    f"{CONFIG.POSTGRES_PORT}/{CONFIG.POSTGRES_DB}"
)

engine = create_engine(URL_DB, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """Inyector de dependencias para sesiones de base de datos en FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crea todas las tablas registradas en la base de datos PostgreSQL.
    Importa todos los modelos mapeados e imprime el estado detallado.
    """
    print(f"[*] Conectando a PostgreSQL en {CONFIG.POSTGRES_HOST}:{CONFIG.POSTGRES_PORT}/{CONFIG.POSTGRES_DB}...")

    try:
        # Importar todos los modelos para registrarlos en Base.metadata
        import db.template.rol          # noqa: F401
        import db.template.user         # noqa: F401
        import db.template.tecnicojefe  # noqa: F401
        import db.template.tecnico      # noqa: F401
        import db.template.empleado     # noqa: F401

        # Crear tablas en el orden correcto resolviendo dependencias de FK
        Base.metadata.create_all(bind=engine)

        # Inspeccionar y verificar las tablas existentes
        inspector = inspect(engine)
        tablas_existentes = inspector.get_table_names()

        print("[+] Tablas creadas / verificadas exitosamente:")
        for tabla in tablas_existentes:
            columnas = [col["name"] for col in inspector.get_columns(tabla)]
            print(f"    - {tabla}: ({', '.join(columnas)})")

    except Exception as exc:
        print(f"[!] Error al crear las tablas en la base de datos: {exc}", file=sys.stderr)
        raise exc