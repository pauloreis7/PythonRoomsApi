from typing import List

from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_setup import get_db
from pydantic_schemas.user import UserCreate, User, UserPatch

from pydantic_schemas.course import Course
from api.utils.users import (
    get_user_by_id,
    get_user_by_email,
    get_users,
    create_db_user,
    patch_db_user,
    delete_db_user,
)

from api.utils.courses import get_user_courses

users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
async def read_users(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: Session = Depends(get_db),
):
    """Get all users list"""

    users = get_users(session=db_session, skip=skip, limit=limit)

    return users


@users_router.get("/users/{user_id}", response_model=User)
async def find_user(
    user_id: int = Path(..., description="User id to retrieve", gt=0),
    db_session: Session = Depends(get_db),
):
    """Find a user"""

    check_user_exists = get_user_by_id(session=db_session, user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    return check_user_exists


@users_router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(
    user_id: int = Path(..., description="User id to retrieve courses"),
    db_session: Session = Depends(get_db),
):
    """Find user's course"""

    check_user_exists = get_user_by_id(session=db_session, user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_courses = get_user_courses(session=db_session, user_id=user_id)

    return user_courses


@users_router.post("/users", response_model=bool, status_code=201)
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
    db_session: Session = Depends(get_db),
):
    """Create a user"""

    check_user_exists = get_user_by_email(session=db_session, email=user.email)

    if check_user_exists:
        raise HTTPException(status_code=400, detail="User already exists!")

    create_db_user_response = create_db_user(session=db_session, user=user)

    return create_db_user_response


@users_router.patch("/users/{user_id}", response_model=bool)
async def patch_user(
    user_id: int = Path(..., description="User id to patch", gt=0),
    user: UserPatch = Body(..., description="User data to patch"),
    db_session: Session = Depends(get_db),
):
    """Patch a user"""

    check_user_exists = get_user_by_id(session=db_session, user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    patch_db_user_response = patch_db_user(
        session=db_session, user_id=user_id, user=user
    )

    return patch_db_user_response


@users_router.delete("/users/{user_id}", response_model=bool)
async def delete_user(
    user_id: int = Path(..., description="User id to delete", gt=0),
    db_session: Session = Depends(get_db),
):
    """Delete a user"""

    check_user_exists = get_user_by_id(session=db_session, user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    delete_db_user_response = delete_db_user(session=db_session, user_id=user_id)

    return delete_db_user_response
