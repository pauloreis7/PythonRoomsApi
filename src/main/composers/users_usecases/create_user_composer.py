from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.create_user_collector import CreateUserCollector
from src.presenters.controllers import CreateUserCollectorController


def create_user_composer():
    """create user composer"""

    infra = UsersRepository()
    use_case = CreateUserCollector(infra)
    controller = CreateUserCollectorController(use_case)

    return controller
