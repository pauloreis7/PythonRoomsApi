from sqlalchemy.orm import Session

from database.models.course import Course
from pydantic_schemas.course import CourseCreate, CoursePatch


def get_course_by_id(session: Session, course_id: int):
    """Get a course by id"""

    course = session.query(Course).filter(Course.id == course_id).first()

    return course


def get_course_by_title(session: Session, course_title: str):
    """Get a course by title"""

    course = session.query(Course).filter(Course.title == course_title).first()

    return course


def get_courses(session: Session, skip: int = 0, limit: int = 100):
    """Get all courses list"""

    courses = session.query(Course).offset(skip).limit(limit).all()

    return courses


def get_user_courses(session: Session, user_id: int):
    """Get a user's courses"""

    courses = session.query(Course).filter(Course.user_id == user_id).all()

    return courses


def create_course(session: Session, course: CourseCreate):
    """Create a course"""

    created_course = Course(
        title=course.title, description=course.description, user_id=course.user_id
    )

    session.add(created_course)
    session.commit()
    session.refresh(created_course)

    return True


def patch_course(session: Session, course_id: int, course: CoursePatch):
    """Patch a course"""

    session.query(Course).filter(Course.id == course_id).update(
        {
            Course.title: course.title,
            Course.description: course.description,
        }
    )

    session.commit()

    return True


def delete_db_course(session: Session, course_id: int):
    """Delete a course"""

    session.query(Course).filter(Course.id == course_id).delete()

    session.commit()

    return True
