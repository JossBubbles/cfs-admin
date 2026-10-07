from fastapi import APIRouter
from config.classRequest import LoginRequest


router = APIRouter()


@router.post("/login")
def login(data: LoginRequest):
    
    print(data.username, "--", data.password)

    from db.connect import engine

    try:
        with engine.connect() as connection:
            print("✅ Conectado a PostgreSQL")
    except Exception as e:
        print("❌ Error:", e)
    return { "ok": "login correcto" }