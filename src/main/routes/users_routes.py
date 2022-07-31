from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.course import Course
from src.domain.models.user import User, UserCreate, UserPatch
from src.infra.config.connection import get_db
from src.presenters.errors.error_controller import handle_errors
from src.main.composers.users_composers.paginate_users_composer import (
    paginate_users_composer,
)
from src.main.composers.users_composers.find_user_by_id_composer import (
    find_user_by_id_composer,
)
from src.main.composers.users_composers.find_user_courses_composer import (
    find_user_courses_composer,
)
from src.main.composers.users_composers.create_user_composer import create_user_composer
from src.main.composers.users_composers.patch_user_composer import patch_user_composer
from src.main.composers.users_composers.delete_user_composer import delete_user_composer

users_router = APIRouter()


@users_router.get("/users", response_model=List[User])
async def read_users(
    skip: int = Query(0, description="skip items in pagination"),
    limit: int = Query(100, description="limit items in pagination"),
    db_session: AsyncSession = Depends(get_db),
):
    """Get all users list"""

    response = None
    paginate_users_controller = paginate_users_composer()

    try:
        response = await paginate_users_controller.handle(
            db_session=db_session, skip=skip, limit=limit
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.get("/users/{user_id}", response_model=User)
async def find_user(
    user_id: int = Path(..., description="User id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Find a user"""

    response = None
    find_user_by_id_controller = find_user_by_id_composer()

    try:
        response = await find_user_by_id_controller.handle(
            db_session=db_session, user_id=user_id
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(
    user_id: int = Path(..., description="User id to retrieve courses"),
    db_session: AsyncSession = Depends(get_db),
):
    """Find user's course"""

    response = None
    find_user_courses_controller = find_user_courses_composer()

    try:
        response = await find_user_courses_controller.handle(
            db_session=db_session, user_id=user_id
        )
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.post("/users", response_model=bool, status_code=201)
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a user"""

    response = None
    create_user_controller = create_user_composer()

    try:
        response = await create_user_controller.handle(db_session=db_session, user=user)
    except Exception as error:
        response = handle_errors(error)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.patch("/users/{user_id}", status_code=204)
async def patch_user(
    user_id: int = Path(..., description="User id to patch", gt=0),
    user: UserPatch = Body(..., description="User data to patch"),
    db_session: AsyncSession = Depends(get_db),
):
    """Patch a user"""

    response = None
    patch_user_controller = patch_user_composer()

    try:
        response = await patch_user_controller.handle(
            db_session=db_session, user_id=user_id, user=user
        )
    except Exception as error:
        response = handle_errors(error)

    return Response(status_code=response["status_code"])


@users_router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="User id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a user"""

    response = None
    delete_user_controller = delete_user_composer()

    try:
        response = await delete_user_controller.handle(
            db_session=db_session, user_id=user_id
        )
    except Exception as error:
        response = handle_errors(error)

    return Response(status_code=response["status_code"])
