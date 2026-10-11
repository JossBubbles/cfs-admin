from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.load import CONFIG

application = FastAPI(title = "cfs-admin")

from api.login import router as router_login




application.add_middleware(
    CORSMiddleware,
    allow_origins = CONFIG.CORS_ALLOW_ORIGINS,
    allow_credentials = CONFIG.CORS_ALLOW_CREDENTIALS,
    allow_methods = CONFIG.CORS_ALLOW_METHODS,
    allow_headers = CONFIG.CORS_ALLOW_HEADERS,
)

application.add_api_route(router_login)