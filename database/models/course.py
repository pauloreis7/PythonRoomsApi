import enum

from sqlalchemy import Enum, Column, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from ..db_setup import Base
from .user import User
from .mixins import Timestamp


class ContentType(enum.Enum):
    """Class to ContentType used in ContentBlock entity"""

    lesson = 1
    quiz = 2
    assignment = 3


class Course(Timestamp, Base):
    """Class to Course entity"""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(URLType, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_by = relationship(User)
    sections = relationship("Section", back_populates="course", uselist=False)


class Section(Timestamp, Base):
    """Class to Section entity"""

    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    contentType: ContentType = Column(Enum(ContentType), nullable=False)
    grade_media = Column(SmallInteger, default=0, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="sections")
