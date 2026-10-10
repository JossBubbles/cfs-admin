import os
from dotenv import load_dotenv


class _Config:
    def __init__(self):
        self.port: int = os.getenv("PORT_APP")
        self.cors_allow_origins: list = os.getenv("CORS_ALLOW_ORIGINS")
        self.cors_allow_methods: list = os.getenv("CORS_ALLOW_METHODS")
        self.cors_allow_headers: list = os.getenv("CORS_ALLOW_HEADERS")
        self.cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS")


load_dotenv()
CONFIG = _Config()