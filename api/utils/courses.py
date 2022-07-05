from sqlalchemy.orm import Session

from database.models.course import Course
from pydantic_schemas.course import CourseCreate, CoursePatch


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()


def get_user_courses(db: Session, user_id: int):
    courses = db.query(Course).filter(Course.user_id == user_id).all()

    return courses


def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        title=course.title, description=course.description, user_id=course.user_id
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def patch_course(db: Session, course_id: int, course: CoursePatch):
    db.query(Course).filter(Course.id == course_id).update(
        {
            Course.title: course.title,
            Course.description: course.description,
        }
    )

    db.commit()

    return True


def delete_db_course(db: Session, course_id: int):
    db.query(Course).filter(Course.id == course_id).delete()

    db.commit()

    return True
