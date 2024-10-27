from fastapi import FastAPI
from app.routers import user_router
from db.database import engine, Base

app = FastAPI()

app.include_router(user_router.router, prefix="/api", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ISLAMEET API!"}