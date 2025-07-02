from loguru import logger

from src.admin.application.interfaces.admin_data_storage import IAdminDataStorage
from src.admin.application.interfaces.repository import IAdminRepository
from src.admin.application.use_cases.get_connected_apps import GetConnectedAppsUseCase
from src.admin.application.use_cases.get_current_api_id import GetCurrentApiIdUseCase
from src.admin.domain.exceptions import AdminException


class AdminAdapter:
    def __init__(self, repository: IAdminRepository, storage: IAdminDataStorage):
        self.repository = repository
        self.storage = storage

    async def initialize(self):
        """Call only once at application startup"""
        api_id = await GetCurrentApiIdUseCase(self.repository).execute()
        connections = await GetConnectedAppsUseCase(self.repository).execute(api_id)
        await self.storage.store_app_connections(connections)

    async def authenticate_application(self, token: str, app_bundle: str | None = None):
        await self.initialize()
        if app_bundle is not None:
            connection = await self.storage.get_app_connection_by_bundle(app_bundle)
        else:
            connection = await self.storage.get_app_connection_by_token(token)
        logger.debug(f"connection: {connection} token: {token}")

        if connection is None:
            raise AdminException("Connection not found")
        if token != connection.api_token:
            raise AdminException("Invalid token")
