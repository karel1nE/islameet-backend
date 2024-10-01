import asyncio

from sqlalchemy import select
from database import Session, engine, Base
from models import UsersOrm

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def add_user(username: str):
    async with Session() as session:
        user = UsersOrm(username=username)
        session.add(user)
        await session.commit()
        return user.id
        

async def get_user(user_id: int):
    async with Session() as session:
        user = await session.get(UsersOrm, user_id)
        return user  

async def update_user(user_id: int, new_username: str):
    async with Session() as session:
        user = await session.get(UsersOrm, user_id)
        if user:
            user.username = new_username
            await session.commit()
            return user
        return None  

async def delete_user(user_id: int):
    async with Session() as session:
        user = await session.get(UsersOrm, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True  
        return False  
    
async def select_users():
    async with Session() as session:
        query = select(UsersOrm)
        res = await session.execute(query)
        print(res.all())


async def main():
    await create_tables()
    await add_user("Andrey")
    await add_user("Miha")
    await add_user("Egor")
    await add_user("laskdfj")
    await select_users()
    
asyncio.run(main())