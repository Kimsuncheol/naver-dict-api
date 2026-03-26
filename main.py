from fastapi import FastAPI
from routers.index import router as index_router
from routers.dict import router as dict_router
from routers.hybridaction import router as hybridaction_router

app = FastAPI(title="Naver Dictionary API")

app.include_router(index_router)
app.include_router(dict_router)
app.include_router(hybridaction_router)
