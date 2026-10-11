from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.load import CONFIG
import db.template  # noqa: F401 - Carga todos los modelos de base de datos en el registro de SQLAlchemy
from api.login import router as router_login

application = FastAPI(title="cfs-admin")

application.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.CORS_ALLOW_ORIGINS,
    allow_credentials=CONFIG.CORS_ALLOW_CREDENTIALS,
    allow_methods=CONFIG.CORS_ALLOW_METHODS,
    allow_headers=CONFIG.CORS_ALLOW_HEADERS,
)

application.include_router(router_login)