from fastapi import APIRouter, Depends
from ..services.user_service import UserService
from ..schemas.user import UserCreate, User
from db.database import get_db
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return user_service.create_user(user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return user_service.get_user(user_id)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return user_service.update_user(user_id, user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    user_service.delete_user(user_id)
    return {"message": "User deleted"}