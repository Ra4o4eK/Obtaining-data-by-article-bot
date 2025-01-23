from datetime import timedelta

from fastapi import APIRouter

from jwt import create_access_token


router = APIRouter()


@router.post("/token")
async def get_token():
    # Здесь можно добавить логику для проверки, если нужно
    access_token_expires = timedelta(hours=48)
    access_token = create_access_token(
        data={"sub": "your_secret_key"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
