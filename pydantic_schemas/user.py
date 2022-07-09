from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    email: str
    role: int
    first_name: str
    last_name: str
    bio: Optional[str] = None
    is_active: bool

    @validator("role")
    def role_validate_enum(cls, value):
        if value not in [1, 2]:
            raise ValueError("Only role 1 and 2 exists")
        return value


class UserCreate(UserBase):
    ...


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
