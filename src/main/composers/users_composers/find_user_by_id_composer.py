from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.find_user_by_id_collector import (
    FindUserByIdCollector,
)
from src.presenters.controllers import (
    FindUserByIdCollectorController,
)


def find_user_by_id_composer():
    """find user by id composer"""

    infra = UsersRepository()
    use_case = FindUserByIdCollector(infra)
    controller = FindUserByIdCollectorController(use_case)

    return controller
