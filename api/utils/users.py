from sqlalchemy import select

from database.models.user import User
from api.config.connection import session


# def get_user_by_id(session: Session, user_id: int):
#     """Get a user by id"""

#     user = session.query(User).filter(User.id == user_id).first()

#     return user


# def get_user_by_email(session: Session, email: str):
#     """Get a user by email"""

#     user = session.query(User).filter(User.email == email).first()

#     return user


async def get_users(skip: int = 0, limit: int = 100):
    """Get all users list"""

    async with session() as db_session:
        query = await db_session.execute(select(User).offset(skip).limit(limit))

        users = query.scalars().all()

        return users


# def create_db_user(session: Session, user: UserCreate):
#     """Create a user"""

#     created_user = User(
#         email=user.email,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         bio=user.bio,
#         role=user.role,
#         is_active=user.is_active,
#     )

#     session.add(created_user)
#     session.commit()
#     session.refresh(created_user)

#     return True


# def patch_db_user(session: Session, user_id: int, user: UserPatch):
#     """Patch a user"""

#     session.query(User).filter(User.id == user_id).update(
#         {
#             User.email: user.email,
#             User.role: user.role,
#             User.first_name: user.first_name,
#             User.last_name: user.last_name,
#             User.bio: user.bio,
#         }
#     )

#     session.commit()

#     return True


# def delete_db_user(session: Session, user_id: int):
#     """Delete a user"""

#     session.query(User).filter(User.id == user_id).delete()

#     session.commit()

#     return True
