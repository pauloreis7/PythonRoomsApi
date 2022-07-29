from typing import List
from faker import Faker
from httpx import AsyncClient

from src.pydantic_schemas.course import CourseCreate, CoursePatch


fake = Faker()


def mock_courses():
    """
    mock data for courses
    :return - list with courses dict
    """

    return [
        {
            "id": 1,
            "user_id": 1,
            "description": fake.text(),
            "title": fake.sentence(),
            "url": fake.url(),
            "updated_at": fake.date_time(),
            "created_at": fake.date_time(),
        },
        {
            "id": 2,
            "user_id": 1,
            "description": fake.text(),
            "title": fake.sentence(),
            "url": fake.url(),
            "updated_at": fake.date_time(),
            "created_at": fake.date_time(),
        },
        {
            "id": 3,
            "user_id": 1,
            "description": fake.text(),
            "title": fake.sentence(),
            "url": fake.url(),
            "updated_at": fake.date_time(),
            "created_at": fake.date_time(),
        },
    ]


class CoursesRepositorySpy:
    """Spy to courses repository"""

    def __init__(self) -> None:
        self.get_courses_attributes = {}
        self.get_course_by_id_attributes = {}
        self.get_course_by_title_attributes = {}
        self.get_user_courses_attributes = {}
        self.create_db_course_attributes = {}
        self.patch_db_course_attributes = {}
        self.delete_db_course_attributes = {}

    async def get_courses(
        self, _: AsyncClient, skip: int = 0, limit: int = 100
    ) -> List[dict]:
        """Get all courses list test"""

        self.get_courses_attributes["skip"] = skip
        self.get_courses_attributes["limit"] = limit

        return mock_courses()

    async def get_course_by_id(self, _: AsyncClient, course_id: int) -> dict:
        """Get a course by id test"""

        self.get_course_by_id_attributes["course_id"] = course_id

        courses = mock_courses()

        check_course_exists = None

        for course in courses:
            if course["id"] == course_id:
                check_course_exists = course
                break

        return check_course_exists

    async def get_course_by_title(self, _: AsyncClient, course_title: str) -> dict:
        """Get a course by title test"""

        self.get_course_by_title_attributes["course_title"] = course_title

        courses = mock_courses()

        check_course_exists = None

        for course in courses:
            if course["title"] == course_title:
                check_course_exists = course
                break

        return check_course_exists

    async def get_user_courses(self, _: AsyncClient, user_id: int) -> List[dict]:
        """Get a user's courses test"""

        self.get_user_courses_attributes["user_id"] = user_id

        courses = mock_courses()

        users_courses = []

        for course in courses:
            if course["user_id"] == user_id:
                users_courses.append(course)
                break

        return users_courses

    async def create_db_course(self, _: AsyncClient, course: CourseCreate) -> bool:
        """Create a course test"""

        self.create_db_course_attributes["title"] = course.title
        self.create_db_course_attributes["description"] = course.description
        self.create_db_course_attributes["url"] = course.url
        self.create_db_course_attributes["user_id"] = course.user_id

        return True

    async def patch_db_course(
        self, _: AsyncClient, course_id: int, course: CoursePatch
    ) -> None:
        """Patch a course test"""

        self.patch_db_course_attributes["course_id"] = course_id
        self.patch_db_course_attributes["title"] = course.title
        self.patch_db_course_attributes["description"] = course.description
        self.patch_db_course_attributes["url"] = course.url
        self.patch_db_course_attributes["user_id"] = course.user_id

        courses_mock = mock_courses()

        for course_mock in courses_mock:
            if course_mock["id"] == course_id:
                course_mock = course
                break

        return

    async def delete_db_course(self, _: AsyncClient, course_id: int) -> None:
        """Delete a course test"""

        self.delete_db_course_attributes["course_id"] = course_id

        courses = mock_courses()

        for index, _ in enumerate(courses):
            if courses[index]["id"] == course_id:
                del courses[index]
                break

        return
