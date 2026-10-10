from fastapi import APIRouter

from config.request import LoginRequest

router = APIRouter()


@router.post("/")
def login(data: LoginRequest):
    print(data.username, "--", data.password)

    return {
        "ok": False,
        "token": "sdfgfdsa"
    }