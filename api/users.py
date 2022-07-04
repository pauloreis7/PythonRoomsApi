from typing import List

from fastapi import APIRouter, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_setup import get_db
from pydantic_schemas.user import UserCreate, User
from pydantic_schemas.course import Course
from api.utils.users import get_user, get_user_by_email, get_users, create_user
from api.utils.courses import get_user_courses

users_router = APIRouter()

@users_router.get('/users', response_model=List[User])
async def read_users(
    skip: int = Query(0, description='skip items in pagination'),
    limit: int = Query(100, description='limit items in pagination'),
    db: Session = Depends(get_db)
):
    """Get all users list"""

    users = get_users(db, skip=skip, limit=limit)

    return users

@users_router.get('/users/{user_id}', response_model=User)
async def find_user(
    user_id: int = Path(..., description='User id to retrieve'),
    db: Session = Depends(get_db)
):
    """Find a user"""

    find_user_in_db = get_user(db=db, user_id=user_id)

    if find_user_in_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    return find_user_in_db

@users_router.post('/users', response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a user"""

    check_user_exists = get_user_by_email(db=db, email=user.email)

    if check_user_exists:
        raise HTTPException(status_code=400, detail="User already exists!")

    return create_user(db=db, user=user)

@users_router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
    courses = get_user_courses(db=db, user_id=user_id)
    return courses
