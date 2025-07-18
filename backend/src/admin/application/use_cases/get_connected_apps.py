from uuid import UUID

from src.admin.application.interfaces.repository import IAdminRepository
from src.admin.domain.dtos import ApiConnectionReadDTO
from src.admin.domain.entities import ApiConnection


class GetConnectedAppsUseCase:
    def __init__(self, repository: IAdminRepository):
        self.repository = repository

    async def execute(self, api_id: UUID) -> list[ApiConnectionReadDTO]:
        connections = await self.repository.get_connections(api_id)
        app_id_to_bundle = await self._get_app_id_to_bundle_dict(connections)
        return [ApiConnectionReadDTO(**connection.model_dump(), app_bundle=app_id_to_bundle[connection.app_id]) for connection in connections]

    async def _get_app_id_to_bundle_dict(self, connections: list[ApiConnection]) -> dict[UUID, str]:
        app_id_to_bundle = {}
        for conn in connections:
            if conn.app_id in app_id_to_bundle:
                continue
            app = await self.repository.get_app_by_id(conn.app_id)
            app_id_to_bundle[conn.app_id] = app.bundle
        return app_id_to_bundle