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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    print(f"[*] Conectando a PostgreSQL en {CONFIG.POSTGRES_HOST}:{CONFIG.POSTGRES_PORT}/{CONFIG.POSTGRES_DB}...")

    try:
        import db.templates.rol        
        import db.templates.user        
        import db.templates.tecnicojefe 
        import db.templates.tecnico      
        import db.templates.empleado    

        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        tablas_existentes = inspector.get_table_names()

        print("[+] Tablas creadas / verificadas exitosamente:")
        for tabla in tablas_existentes:
            columnas = [col["name"] for col in inspector.get_columns(tabla)]
            print(f"    - {tabla}: ({', '.join(columnas)})")

    except Exception as exc:
        print(f"[!] Error al crear las tablas en la base de datos: {exc}", file=sys.stderr)
        raise exc