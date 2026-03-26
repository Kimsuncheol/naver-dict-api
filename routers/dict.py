from fastapi import APIRouter, HTTPException, Query
try:
    from naver_dict_api import NaverDictError
except ModuleNotFoundError:
    class NaverDictError(Exception):
        pass
from services.dict import get_dict_types, lookup

router = APIRouter(prefix="/dict", tags=["dictionary"])


@router.get("/types")
def list_dict_types():
    return get_dict_types()


@router.get("/search")
def search(
    query: str = Query(..., description="Word or character to search"),
    dict_type: str = Query("english", description="Dictionary type (e.g. korean, english, japanese, hanja)"),
    search_mode: str = Query("simple", description="Search mode: simple or detailed"),
):
    try:
                # If the external dependency is missing, the service layer will usually
        # fail as well. This keeps the API response clearer than an import-time crash.
        if NaverDictError is Exception:
            raise HTTPException(
                status_code=500,
                detail="Missing dependency: install the package that provides `naver_dict_api` before using /dict/search.",
            )
        entry = lookup(query, dict_type, search_mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NaverDictError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return entry.to_dict()
