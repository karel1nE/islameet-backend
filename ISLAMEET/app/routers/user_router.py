from fastapi import APIRouter, Depends, HTTPException
from ..services.user_service import UserService
from ..schemas.user import UserCreate, User
from db.database import get_db
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository

router = APIRouter()

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    try:
        return user_service.create_user(user)
    except Exception:
        raise HTTPException(status_code=400, detail="An error occurred while creating the user.")

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    try:
        user = user_service.get_user(user_id)
        if user is None:
            raise UserNotFoundException()
        return user
    except Exception:
        raise HTTPException(status_code=400, detail="An error occurred while retrieving the user.")

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    try:
        updated_user = user_service.update_user(user_id, user)
        if updated_user is None:
            raise UserNotFoundException()
        return updated_user
    except Exception:
        raise HTTPException(status_code=400, detail="An error occurred while updating the user.")

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    try:
        user_service.delete_user(user_id)
        return {"message": "User deleted"}
    except Exception:
        raise UserNotFoundException()