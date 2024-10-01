from typing import Optional
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import datetime

time_now = lambda: datetime.datetime.now(datetime.timezone.utc)

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    birthday: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)  
    city: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)  

class ComplaintsOrm(Base):
    __tablename__ = 'complaints'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  
    from_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)  
    time_send: Mapped[datetime.datetime] = mapped_column(DateTime, default=time_now)  

    from_user = relationship("UsersOrm", foreign_keys=[from_user_id])
    to_user = relationship("UsersOrm", foreign_keys=[to_user_id])