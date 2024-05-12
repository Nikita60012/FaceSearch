from fastapi import APIRouter

router = APIRouter(
    prefix='/utils',
    tags=['Утилиты']
)


@router.get("/check_connection")
async def check_connection():
    return True
