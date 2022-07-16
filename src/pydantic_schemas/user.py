from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    """User Base Model"""

    email: str
    role: int
    first_name: str
    last_name: str
    bio: Optional[str] = None
    is_active: bool

    @validator("role")
    @classmethod
    def role_validate_enum(cls, value):
        """Validate User role enum value"""

        if value not in [1, 2]:
            raise ValueError("Only role 1 and 2 exists")
        return value


class UserCreate(UserBase):
    """Create User Model Data"""


class UserPatch(BaseModel):
    """Patch User Model Data"""

    email: str
    role: int
    first_name: str
    last_name: str
    bio: Optional[str] = None

    @validator("role")
    @classmethod
    def role_validate_enum(cls, value):
        """Validate User role enum value"""

        if value not in [1, 2]:
            raise ValueError("Only role 1 and 2 exists")
        return value


class User(UserBase):
    """User Model read"""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Orm serialized read"""

        orm_mode = True
