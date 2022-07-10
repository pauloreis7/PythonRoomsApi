from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Query, Response

# from database.db_setup import get_db
from pydantic_schemas.user import User, UserCreate, UserPatch

from api.utils.users import (
    create_db_user,
    delete_db_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    patch_db_user,
)


users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
async def read_users(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
):
    """Get all users list"""

    users = await get_users(skip=skip, limit=limit)

    return users


@users_router.get("/users/{user_id}", response_model=User)
async def find_user(
    user_id: int = Path(..., description="User id to retrieve", gt=0),
):
    """Find a user"""

    check_user_exists = await get_user_by_id(user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    return check_user_exists


# @users_router.get("/users/{user_id}/courses", response_model=List[Course])
# async def read_user_courses(
#     user_id: int = Path(..., description="User id to retrieve courses"),
# ):
#     """Find user's course"""

#     check_user_exists = await get_user_by_id(user_id=user_id)

#     if check_user_exists is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     user_courses = await get_user_courses(user_id=user_id)

#     return user_courses


@users_router.post("/users", response_model=bool, status_code=201)
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
):
    """Create a user"""

    check_user_exists = await get_user_by_email(email=user.email)

    if check_user_exists:
        raise HTTPException(status_code=400, detail="User already exists!")

    create_db_user_response = await create_db_user(user=user)

    return create_db_user_response


@users_router.patch("/users/{user_id}", status_code=204)
async def patch_user(
    user_id: int = Path(..., description="User id to patch", gt=0),
    user: UserPatch = Body(..., description="User data to patch"),
):
    """Patch a user"""

    check_user_exists = await get_user_by_id(user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    await patch_db_user(user_id=user_id, user=user)

    return Response(status_code=204)


@users_router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="User id to delete", gt=0),
):
    """Delete a user"""

    check_user_exists = await get_user_by_id(user_id=user_id)

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_db_user(user_id=user_id)

    return Response(status_code=204)
