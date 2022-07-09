from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    role: int
    first_name: str
    last_name: str
    bio: Optional[str] = None
    is_active: bool


class UserCreate(UserBase):
    ...


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
