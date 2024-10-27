from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, user_data: UserCreate):
        user = self.get_user(user_id)
        for key, value in user_data.dict().items():
            setattr(user, key, value)
        self.db.commit()
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()