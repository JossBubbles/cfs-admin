from config.load import CONFIG

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DB = (
    f"postgresql+psycopg://{CONFIG.POSTGRES_USER}:{CONFIG.POSTGRES_PASSWORD}@{CONFIG.POSTGRES_HOST}:"
    f"{CONFIG.POSTGRES_PORT}/{CONFIG.POSTGRES_DB}"
)

engine = create_engine(URL_DB)
SessionLocal = sessionmaker( bind = engine, autoflush = False, autocommit = False )



def create_tables():
    return