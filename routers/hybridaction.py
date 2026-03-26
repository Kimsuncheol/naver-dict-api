from fastapi import APIRouter

router = APIRouter(prefix="/hybridaction",tags=["hybridaction"])


@router.get("/hybridaction/{path:path}")
async def ignore_tracker(path: str):
    return {"status": "ignored"}