from fastapi import APIRouter

router = APIRouter(tags=["index"])


@router.get("/")
def index():
    return {
        "name": "Naver Dictionary API",
        "endpoints": [
            {"method": "GET", "path": "/dict/types", "description": "List available dictionary types"},
            {"method": "GET", "path": "/dict/search", "description": "Search a word in a dictionary"},
        ],
    }
