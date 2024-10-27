from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: UserCreate):
        return self.user_repository.create_user(user)

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)

    def update_user(self, user_id: int, user_data: UserCreate):
        return self.user_repository.update_user(user_id, user_data)

    def delete_user(self, user_id: int):
        return self.user_repository.delete_user(user_id)