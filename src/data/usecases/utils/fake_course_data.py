from faker import Faker

from src.pydantic_schemas.course import CourseCreate

fake = Faker()


def create_fake_course(user_id: int = 1):
    """Util to create a fake course"""

    course = CourseCreate(
        title=fake.sentence(),
        description=fake.text(),
        url=fake.url(),
        user_id=user_id,
    )

    return course
