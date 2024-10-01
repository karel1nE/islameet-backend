from typing import List
from fastapi import Depends, FastAPI, HTTPException

from crud import UserCRUD
from schemas import UserCreate, UserRead
from database import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

app = FastAPI(
    title="Islameet"
)  

async def get_db():
    async with Session() as session:
        yield session

@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await UserCRUD.create_user(session, user)

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await UserCRUD.get_user(session, user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_db)):
    return await UserCRUD.get_all_users(session)

@app.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await UserCRUD.update_user(session, user_id, user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    try:
        await UserCRUD.delete_user(session, user_id)
        return {"detail": "User deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")