import abc
from uuid import UUID

from src.admin.domain.dtos import ApiConnectionReadDTO
from src.admin.domain.entities import ApiConnection


class IAdminDataStorage(abc.ABC):
    @abc.abstractmethod
    async def store_app_connections(self, connections: list[ApiConnectionReadDTO]) -> None: ...

    @abc.abstractmethod
    async def get_app_connection_by_bundle(self, app_bundle: str) -> ApiConnectionReadDTO | None: ...

    @abc.abstractmethod
    async def get_app_connection_by_token(self, api_token: str) -> ApiConnectionReadDTO | None: ...