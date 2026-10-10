from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.load import CONFIG

application = FastAPI(title = "cfs-admin")

from api.login import router as router_login




application.add_middleware(
    CORSMiddleware,
    allow_origins = CONFIG.cors_allow_origins,
    allow_credentials = CONFIG.cors_allow_credentials,
    allow_methods = CONFIG.cors_allow_methods,
    allow_headers = CONFIG.cors_allow_headers,
)

application.add_api_route(router_login)