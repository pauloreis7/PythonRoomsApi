from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class CourseBase(BaseModel):
    """Course Base Model"""

    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    user_id: int


class CourseCreate(CourseBase):
    """Create Course Model Data"""


class CoursePatch(BaseModel):
    """Patch Course Model Data"""

    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    user_id: int


class Course(CourseBase):
    """Course Model read"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Orm serialized read"""

        orm_mode = True
