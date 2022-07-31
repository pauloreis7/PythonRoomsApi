from faker import Faker

from src.domain.models.user import UserCreate, UserPatch

fake = Faker()


def create_fake_user():
    """Util to create a fake user"""

    user = UserCreate(
        email=fake.email(),
        role=1,
        first_name=fake.name(),
        last_name=fake.name(),
        bio=fake.text(),
        is_active=fake.boolean(),
    )

    return user


def patch_fake_user():
    """Util to patch a fake user"""

    user = UserPatch(
        email=fake.email(),
        role=1,
        first_name=fake.name(),
        last_name=fake.name(),
        bio=fake.text(),
    )

    return user
