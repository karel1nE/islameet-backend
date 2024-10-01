from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Annotated, Optional

class UserCreate(BaseModel):
    username: Annotated[str, constr(min_length=1, max_length=256)]
    email: EmailStr
    description: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[str] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    description: Optional[str]
    birthday: Optional[date]
    city: Optional[str]

    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    from_user_id: int
    to_user_id: int
    description: Annotated[str, constr(min_length=1, max_length=256)]
    status: Optional[str] = "pending"  

class ComplaintRead(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    description: str
    status: str
    time_send: str  

    class Config:
        from_attributes = True