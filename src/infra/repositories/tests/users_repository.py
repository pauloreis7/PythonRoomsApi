from typing import List
from faker import Faker

from src.pydantic_schemas.user import UserCreate, UserPatch

fake = Faker()


def mock_users():
    """
    mock data for users
    :return - list with users dict
    """

    return [
        {
            "id": 1,
            "first_name": fake.name(),
            "bio": fake.text(),
            "is_active": fake.unique.boolean(),
            "email": "test01@email.com",
            "last_name": fake.name(),
            "role": 1,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
        {
            "id": 2,
            "first_name": fake.name(),
            "bio": fake.text(),
            "is_active": fake.unique.boolean(),
            "email": "test02@email.com",
            "last_name": fake.name(),
            "role": 1,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
        {
            "id": 3,
            "first_name": fake.name(),
            "bio": fake.text(),
            "is_active": fake.unique.boolean(),
            "email": "test03@email.com",
            "last_name": fake.name(),
            "role": 2,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        },
    ]


class UsersRepositorySpy:
    """Spy to users repository"""

    def __init__(self) -> None:
        self.get_users_attributes = {}
        self.get_user_by_id_attributes = {}
        self.get_user_by_email_attributes = {}
        self.create_db_user_attributes = {}
        self.patch_db_user_attributes = {}
        self.delete_db_user_attributes = {}

    def get_users(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all users list test"""

        self.get_users_attributes["skip"] = skip
        self.get_users_attributes["limit"] = limit

        return mock_users()

    async def get_user_by_id(self, user_id: int) -> dict:
        """Get a user by id test"""

        self.get_user_by_id_attributes["user_id"] = user_id

        users = mock_users()

        check_user_exists = None

        for user in users:
            if user["id"] == user_id:
                check_user_exists = user
                break

        return check_user_exists

    async def get_user_by_email(self, user_email: str) -> dict:
        """Get a user by email test"""

        self.get_user_by_email_attributes["user_email"] = user_email

        users = mock_users()

        check_user_exists = None

        for user in users:
            if user["email"] == user_email:
                check_user_exists = user
                break

        return check_user_exists

    async def create_db_user(self, user: UserCreate) -> bool:
        """Create a user test"""

        self.create_db_user_attributes["email"] = user.email
        self.create_db_user_attributes["role"] = user.role
        self.create_db_user_attributes["first_name"] = user.first_name
        self.create_db_user_attributes["last_name"] = user.last_name
        self.create_db_user_attributes["bio"] = user.bio
        self.create_db_user_attributes["is_active"] = user.is_active

        return True

    async def patch_db_user(self, user_id: int, user: UserPatch) -> None:
        """Patch a user test"""

        self.patch_db_user_attributes["user_id"] = user_id
        self.patch_db_user_attributes["email"] = user.email
        self.patch_db_user_attributes["role"] = user.role
        self.patch_db_user_attributes["first_name"] = user.first_name
        self.patch_db_user_attributes["last_name"] = user.last_name
        self.patch_db_user_attributes["bio"] = user.bio

        users_mock = mock_users()

        for user_mock in users_mock:
            if user_mock["id"] == user_id:
                user_mock = user
                break

        return

    async def delete_db_user(self, user_id: int) -> None:
        """Delete a user test"""

        self.delete_db_user_attributes["user_id"] = user_id

        users = mock_users()

        for index, _ in enumerate(users):
            if users[index]["id"] == user_id:
                del users[index]
                break

        return
