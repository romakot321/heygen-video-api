import abc
from uuid import UUID

from src.integration.domain.entities import AvatarCreate, Avatar, AvatarUpdate


class IAvatarRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: AvatarCreate) -> Avatar: ...

    @abc.abstractmethod
    async def get_list_by_user(self, user_id: str, app_bundle: str) -> list[Avatar]: ...

    @abc.abstractmethod
    async def update_by_pk(self, pk: UUID, data: AvatarUpdate) -> None: ...