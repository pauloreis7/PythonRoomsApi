from sqlalchemy.orm import Session

from database.models.user import User
from pydantic_schemas.user import UserCreate


def get_user_by_id(session: Session, user_id: int):
    """Get a user by id"""

    user = session.query(User).filter(User.id == user_id).first()

    return user


def get_user_by_email(session: Session, email: str):
    """Get a user by email"""

    user = session.query(User).filter(User.email == email).first()

    return user


def get_users(session: Session, skip: int = 0, limit: int = 100):
    """Get all users list"""

    users = session.query(User).offset(skip).limit(limit).all()

    return users


def create_user(session: Session, user: UserCreate):
    """Create a user"""

    created_user = User(email=user.email, role=user.role)

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user
