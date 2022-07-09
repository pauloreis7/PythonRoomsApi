from typing import Optional

from pydantic import BaseModel


class SectionBase(BaseModel):
    title: str
    description: Optional[str] = None

    grade_media: Optional[int] = 0
    course_id: int


class SectionCreate(SectionBase):
    ...


class SectionPatch(SectionBase):
    title: str
    description: Optional[str] = None

    grade_media: Optional[int] = 0


class Section(SectionBase):
    id: int

    class Config:
        orm_mode = True
