from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.paginate_users_collector import (
    PaginateUsersCollector,
)
from src.presenters.controllers import (
    PaginateUsersCollectorController,
)


def paginate_users_composer():
    """paginate users composer"""

    infra = UsersRepository()
    use_case = PaginateUsersCollector(infra)
    controller = PaginateUsersCollectorController(use_case)

    return controller
