from fastapi import FastAPI
from routers.dict import router as dict_router

app = FastAPI(title="Naver Dictionary API")

app.include_router(dict_router)
