from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


# pylint: disable=E0213
class SectionBase(BaseModel):
    """Section Base Model"""

    title: str
    description: Optional[str] = None
    content_type: int
    grade_media: Optional[int] = 0
    course_id: int

    @validator("content_type")
    @classmethod
    def content_type_validate_enum(cls, value):
        """Validate Section content_type enum value"""

        if value not in [1, 2, 3]:
            raise ValueError("Only content type 1, 2 and 3 exists")
        return value


class SectionCreate(SectionBase):
    """Create Section Model Data"""


class SectionPatch(BaseModel):
    """Patch Section Model Data"""

    title: str
    description: Optional[str] = None
    content_type: int
    grade_media: Optional[int] = 0

    @validator("content_type")
    @classmethod
    def content_type_validate_enum(cls, value):
        """Validate Section content_type enum value"""

        if value not in [1, 2, 3]:
            raise ValueError("Only content type 1, 2 and 3 exists")
        return value


class Section(SectionBase):
    """Section Model read"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Orm serialized read"""

        orm_mode = True
