from src.admin.application.interfaces.admin_data_storage import IAdminDataStorage
from src.admin.domain.dtos import ApiConnectionReadDTO

_storage: list[ApiConnectionReadDTO] = []


class InMemoryAdminDataStorage(IAdminDataStorage):
    storage = _storage

    def __init__(self):
        pass

    async def store_app_connections(self, connections: list[ApiConnectionReadDTO]) -> None:
        self.storage.extend(connections)

    async def get_app_connection_by_bundle(self, app_bundle: str) -> ApiConnectionReadDTO | None:
        for connection in self.storage:
            if connection.app_bundle == app_bundle:
                return connection
        return None

    async def get_app_connection_by_token(self, api_token: str) -> ApiConnectionReadDTO | None:
        for connection in self.storage:
            if connection.api_token == api_token:
                return connection
        return None
