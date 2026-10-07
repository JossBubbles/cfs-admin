from fastapi import FastAPI
from api.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware

Aplicacion = FastAPI(title = "cfs-admin")

Aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET", "POST"],
    allow_headers = ["Content-Type", "Authorization"] 
)

# apis de login y raiz
Aplicacion.include_router(login_router)