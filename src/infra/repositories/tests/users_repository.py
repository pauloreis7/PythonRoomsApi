from typing import List
from faker import Faker
from httpx import AsyncClient

from src.pydantic_schemas.user import UserCreate, UserPatch
from src.data.interfaces.users_repository import UsersRepositoryInterface

fake = Faker()


class UsersRepositorySpy(UsersRepositoryInterface):
    """Spy to users repository"""

    def __init__(self) -> None:
        self.users = []
        self.get_users_attributes = {}
        self.get_user_by_id_attributes = {}
        self.get_user_by_email_attributes = {}
        self.create_db_user_attributes = {}
        self.patch_db_user_attributes = {}
        self.delete_db_user_attributes = {}

    async def get_users(
        self, _: AsyncClient, skip: int = 0, limit: int = 100
    ) -> List[dict]:
        """Get all users list test"""

        self.get_users_attributes["skip"] = skip
        self.get_users_attributes["limit"] = limit

        users = self.users

        return users

    async def get_user_by_id(self, _: AsyncClient, user_id: int) -> dict:
        """Get a user by id test"""

        self.get_user_by_id_attributes["user_id"] = user_id

        check_user_exists = None

        for user in self.users:
            if user["id"] == user_id:
                check_user_exists = user
                break

        return check_user_exists

    async def get_user_by_email(self, _: AsyncClient, user_email: str) -> dict:
        """Get a user by email test"""

        self.get_user_by_email_attributes["user_email"] = user_email

        check_user_exists = None

        for user in self.users:
            if user["email"] == user_email:
                check_user_exists = user
                break

        return check_user_exists

    async def create_db_user(self, _: AsyncClient, user: UserCreate) -> dict:
        """Create a user test"""

        self.create_db_user_attributes["email"] = user.email
        self.create_db_user_attributes["role"] = user.role
        self.create_db_user_attributes["first_name"] = user.first_name
        self.create_db_user_attributes["last_name"] = user.last_name
        self.create_db_user_attributes["bio"] = user.bio
        self.create_db_user_attributes["is_active"] = user.is_active

        fake_user = {
            "id": fake.random_int(),
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "is_active": user.is_active,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        }

        self.users.append(fake_user)

        return fake_user

    async def patch_db_user(
        self, _: AsyncClient, user_id: int, user: UserPatch
    ) -> dict:
        """Patch a user test"""

        self.patch_db_user_attributes["user_id"] = user_id
        self.patch_db_user_attributes["email"] = user.email
        self.patch_db_user_attributes["role"] = user.role
        self.patch_db_user_attributes["first_name"] = user.first_name
        self.patch_db_user_attributes["last_name"] = user.last_name
        self.patch_db_user_attributes["bio"] = user.bio

        fake_user = {
            "id": fake.random_int(),
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "is_active": user.is_active,
            "created_at": fake.date_time(),
            "updated_at": fake.date_time(),
        }

        for user in self.users:
            if user["id"] == user_id:
                user = fake_user
                break

        return fake_user

    async def delete_db_user(self, _: AsyncClient, user_id: int) -> None:
        """Delete a user test"""

        self.delete_db_user_attributes["user_id"] = user_id

        for index, _ in enumerate(self.users):
            if self.users[index]["id"] == user_id:
                del self.users[index]
                break

        return
