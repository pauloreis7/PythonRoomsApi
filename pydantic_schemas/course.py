from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    user_id: int


class CourseCreate(CourseBase):
    ...


class CoursePatch(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None


class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
