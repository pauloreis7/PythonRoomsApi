from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class SectionBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: int
    grade_media: Optional[int] = 0
    course_id: int

    @validator("content_type")
    def content_type_validate_enum(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError("Only role 1, 2 and 3 exists")
        return value


class SectionCreate(SectionBase):
    ...


class SectionPatch(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: int
    grade_media: Optional[int] = 0


class Section(SectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
