import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship

from api.config.base import Base
from .mixins import Timestamp


class Role(enum.IntEnum):
    """Class to Role used in User entity"""

    teacher = 1
    student = 2


class User(Timestamp, Base):
    """Class to User entity"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    bio = Column(Text, nullable=True)
    role: Role = Column(Enum(Role))
    is_active = Column(Boolean, default=False)

    courses = relationship("Course", back_populates="created_by")
