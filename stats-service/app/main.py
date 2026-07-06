from fastapi import FastAPI
from app.routers.stats_router import router

app = FastAPI()
app.include_router(router)


@app.get("/ping")
def ping():
    return {"message": "pong"}