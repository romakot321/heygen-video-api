from src.admin.application.interfaces.admin_data_storage import IAdminDataStorage
from src.admin.application.interfaces.repository import IAdminRepository
from src.admin.domain.exceptions import AdminRequestException


class AuthenticateUserUseCase:
    def __init__(self, repository: IAdminRepository, storage: IAdminDataStorage):
        self.repository = repository
        self.storage = storage

    async def execute(self, user_apphud_id: str, app_bundle: str) -> bool:
        connection = await self.storage.get_app_connection_by_bundle(app_bundle)
        try:
            await self.repository.get_user(user_apphud_id, connection.app_id)
        except AdminRequestException:
            return False
        return True