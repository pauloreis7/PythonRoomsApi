from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course
from src.pydantic_schemas.user import User, UserCreate, UserPatch
from src.infra.config.connection import get_db
from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.users_pagination_collector import (
    UsersPaginationCollector,
)


users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
async def read_users(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all users list"""

    infra = UsersRepository()
    use_case = UsersPaginationCollector(infra)

    users = await use_case.users_pagination(db_session, skip=skip, limit=limit)

    return JSONResponse(status_code=200, content=jsonable_encoder(users))


@users_router.get("/users/{user_id}", response_model=User)
async def find_user(
    user_id: int = Path(..., description="User id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Find a user"""

    users_repository = UsersRepository()

    check_user_exists = await users_repository.get_user_by_id(
        db_session, user_id=user_id
    )

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(status_code=200, content=jsonable_encoder(check_user_exists))


@users_router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(
    user_id: int = Path(..., description="User id to retrieve courses"),
    db_session: AsyncSession = Depends(get_db),
):
    """Find user's course"""

    users_repository = UsersRepository()
    courses_repository = CoursesRepository()

    check_user_exists = await users_repository.get_user_by_id(
        db_session, user_id=user_id
    )

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_courses = await courses_repository.get_user_courses(
        db_session, user_id=user_id
    )

    return JSONResponse(status_code=200, content=jsonable_encoder(user_courses))


@users_router.post("/users", response_model=bool, status_code=201)
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a user"""

    users_repository = UsersRepository()

    check_user_exists = await users_repository.get_user_by_email(
        db_session, user_email=user.email
    )

    if check_user_exists:
        raise HTTPException(status_code=400, detail="User already exists!")

    create_db_user_response = await users_repository.create_db_user(
        db_session, user=user
    )

    return JSONResponse(
        status_code=201, content=jsonable_encoder(create_db_user_response)
    )


@users_router.patch("/users/{user_id}", status_code=204)
async def patch_user(
    user_id: int = Path(..., description="User id to patch", gt=0),
    user: UserPatch = Body(..., description="User data to patch"),
    db_session: AsyncSession = Depends(get_db),
):
    """Patch a user"""

    users_repository = UsersRepository()

    check_user_exists = await users_repository.get_user_by_id(
        db_session, user_id=user_id
    )

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    await users_repository.patch_db_user(db_session, user_id=user_id, user=user)

    return Response(status_code=204)


@users_router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="User id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a user"""

    users_repository = UsersRepository()

    check_user_exists = await users_repository.get_user_by_id(
        db_session, user_id=user_id
    )

    if check_user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")

    await users_repository.delete_db_user(db_session, user_id=user_id)

    return Response(status_code=204)
