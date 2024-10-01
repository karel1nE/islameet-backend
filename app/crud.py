from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import List
from sqlalchemy.orm import Session as SyncSession
from schemas import UserCreate, UserRead
from models import UsersOrm

class UserCRUD:

    @staticmethod
    async def create_user(session: AsyncSession, user: UserCreate) -> UserRead:
        new_user = UsersOrm(**user.dict())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserRead.from_orm(new_user)

    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> UserRead:
        result = await session.execute(select(UsersOrm).where(UsersOrm.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise NoResultFound(f"User with id {user_id} not found.")
        return UserRead.from_orm(user)

    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[UserRead]:
        result = await session.execute(select(UsersOrm))
        return [UserRead.from_orm(user) for user in result.scalars().all()]

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, user_data: UserCreate) -> UserRead:
        user = await UserCRUD.get_user(session, user_id)
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return UserRead.from_orm(user)

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> None:
        user = await UserCRUD.get_user(session, user_id)
        await session.delete(user)
        await session.commit()