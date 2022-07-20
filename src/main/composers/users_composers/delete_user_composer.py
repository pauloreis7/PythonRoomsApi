from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.delete_user_collector import DeleteUserCollector
from src.presenters.controllers import DeleteUserCollectorController


def delete_user_composer():
    """delete user composer"""

    infra = UsersRepository()
    use_case = DeleteUserCollector(infra)
    controller = DeleteUserCollectorController(use_case)

    return controller
