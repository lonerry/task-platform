from fastapi import APIRouter

health_check_router = APIRouter()


@health_check_router.get("/health")
async def health():
    return {"status": "ok"}
