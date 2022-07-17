from typing import List

from fastapi import APIRouter, Depends, Body, Path, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.pydantic_schemas.course import Course
from src.pydantic_schemas.user import User, UserCreate, UserPatch
from src.infra.config.connection import get_db
from src.infra.repositories.courses_repository import CoursesRepository
from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.paginate_users_collector import (
    PaginateUsersCollector,
)
from src.data.usecases.users_usecases.find_user_by_id_collector import (
    FindUserByIdCollector,
)
from src.data.usecases.users_usecases.find_user_courses_collector import (
    FindUserCoursesCollector,
)
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.data.usecases.users_usecases.patch_user_collector import PatchUserCollector
from src.data.usecases.users_usecases.delete_user_collector import DeleteUserCollector
from src.presenters.controllers.users_controllers.paginate_users_collector_controller import (
    PaginateUsersCollectorController,
)
from src.presenters.controllers.users_controllers.find_user_by_id_collector_controller import (
    FindUserByIdCollectorController,
)
from src.presenters.controllers.users_controllers.find_user_courses_collector_controller import (
    FindUserCoursesCollectorController,
)
from src.presenters.controllers.users_controllers.create_user_collector_controller import (
    CreateUserCollectorController,
)
from src.presenters.controllers.users_controllers.patch_user_collector_controller import (
    PatchUserCollectorController,
)
from src.presenters.controllers.users_controllers.delete_user_collector_controller import (
    DeleteUserCollectorController,
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
    use_case = PaginateUsersCollector(infra)
    controller = PaginateUsersCollectorController(use_case)

    response = await controller.handle(db_session=db_session, skip=skip, limit=limit)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.get("/users/{user_id}", response_model=User)
async def find_user(
    user_id: int = Path(..., description="User id to retrieve", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Find a user"""

    infra = UsersRepository()
    use_case = FindUserByIdCollector(infra)
    controller = FindUserByIdCollectorController(use_case)

    response = await controller.handle(db_session=db_session, user_id=user_id)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(
    user_id: int = Path(..., description="User id to retrieve courses"),
    db_session: AsyncSession = Depends(get_db),
):
    """Find user's course"""

    users_infra = UsersRepository()
    courses_infra = CoursesRepository()
    use_case = FindUserCoursesCollector(users_infra, courses_infra)
    controller = FindUserCoursesCollectorController(use_case)

    response = await controller.handle(db_session=db_session, user_id=user_id)

    return JSONResponse(
        status_code=response["status_code"], content=jsonable_encoder(response["data"])
    )


@users_router.post("/users", response_model=bool, status_code=201)
async def create_user(
    user: UserCreate = Body(..., description="User data to create"),
    db_session: AsyncSession = Depends(get_db),
):
    """Create a user"""

    infra = UsersRepository()
    use_case = CreateUserCollector(infra)
    controller = CreateUserCollectorController(use_case)

    response = await controller.handle(db_session=db_session, user=user)

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

    infra = UsersRepository()
    use_case = PatchUserCollector(infra)
    controller = PatchUserCollectorController(use_case)

    response = await controller.handle(
        db_session=db_session, user_id=user_id, user=user
    )

    return Response(status_code=response["status_code"])


@users_router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="User id to delete", gt=0),
    db_session: AsyncSession = Depends(get_db),
):
    """Delete a user"""

    infra = UsersRepository()
    use_case = DeleteUserCollector(infra)
    controller = DeleteUserCollectorController(use_case)

    response = await controller.handle(db_session=db_session, user_id=user_id)

    return Response(status_code=response["status_code"])
