from typing import List
from faker import Faker
from httpx import AsyncClient

from src.pydantic_schemas.user import User, UserCreate, UserPatch
from src.data.interfaces.users_repository import UsersRepositoryInterface

fake = Faker()


class UsersRepositorySpy(UsersRepositoryInterface):
    """Spy to users repository"""

    def __init__(self) -> None:
        self.users: List[User] = []
        self.get_users_attributes = {}
        self.get_user_by_id_attributes = {}
        self.get_user_by_email_attributes = {}
        self.create_db_user_attributes = {}
        self.patch_db_user_attributes = {}
        self.delete_db_user_attributes = {}

    async def get_users(
        self, _: AsyncClient, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Get all users list test"""

        self.get_users_attributes["skip"] = skip
        self.get_users_attributes["limit"] = limit

        users = self.users

        return users

    async def get_user_by_id(self, _: AsyncClient, user_id: int) -> User:
        """Get a user by id test"""

        self.get_user_by_id_attributes["user_id"] = user_id

        check_user_exists = None

        for user in self.users:
            if user.id == user_id:
                check_user_exists = user
                break

        return check_user_exists

    async def get_user_by_email(self, _: AsyncClient, user_email: str) -> User:
        """Get a user by email test"""

        self.get_user_by_email_attributes["user_email"] = user_email

        check_user_exists = None

        for user in self.users:
            if user.email == user_email:
                check_user_exists = user
                break

        return check_user_exists

    async def create_db_user(self, _: AsyncClient, user: UserCreate) -> User:
        """Create a user test"""

        self.create_db_user_attributes["email"] = user.email
        self.create_db_user_attributes["role"] = user.role
        self.create_db_user_attributes["first_name"] = user.first_name
        self.create_db_user_attributes["last_name"] = user.last_name
        self.create_db_user_attributes["bio"] = user.bio
        self.create_db_user_attributes["is_active"] = user.is_active

        fake_user = User(
            id=fake.random_int(),
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            bio=user.bio,
            is_active=user.is_active,
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )

        self.users.append(fake_user)

        return fake_user

    async def patch_db_user(
        self, _: AsyncClient, user_id: int, user: UserPatch
    ) -> User:
        """Patch a user test"""

        self.patch_db_user_attributes["user_id"] = user_id
        self.patch_db_user_attributes["email"] = user.email
        self.patch_db_user_attributes["role"] = user.role
        self.patch_db_user_attributes["first_name"] = user.first_name
        self.patch_db_user_attributes["last_name"] = user.last_name
        self.patch_db_user_attributes["bio"] = user.bio

        fake_user = {
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "updated_at": fake.date_time(),
        }

        for index, user_mock in enumerate(self.users):
            if user_mock.id == user_id:
                self.users[index].email = fake_user["email"]
                self.users[index].role = fake_user["role"]
                self.users[index].first_name = fake_user["first_name"]
                self.users[index].last_name = fake_user["last_name"]
                self.users[index].bio = fake_user["bio"]
                self.users[index].updated_at = fake_user["updated_at"]

                break

        return fake_user

    async def delete_db_user(self, _: AsyncClient, user_id: int) -> None:
        """Delete a user test"""

        self.delete_db_user_attributes["user_id"] = user_id

        for index, _ in enumerate(self.users):
            if self.users[index].id == user_id:
                del self.users[index]
                break

        return
