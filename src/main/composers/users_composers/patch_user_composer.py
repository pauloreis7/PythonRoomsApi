from src.infra.repositories.users_repository import UsersRepository
from src.data.usecases.users_usecases.patch_user_collector import PatchUserCollector
from src.presenters.controllers import PatchUserCollectorController


def patch_user_composer():
    """patch user composer"""

    infra = UsersRepository()
    use_case = PatchUserCollector(infra)
    controller = PatchUserCollectorController(use_case)

    return controller
