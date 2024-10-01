from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

DB_URL = f"postgresql+asyncpg://karel1ne:123@localhost:5432/test"

engine = create_async_engine(
    url=DB_URL,
    echo=False,
)

Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
