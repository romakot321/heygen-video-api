from src.integration.domain.dtos import IntegrationAvatarDTO
from src.integration.infrastructure.adapter import HeygenAdapter


class GetAvatarsUseCase:
    def __init__(self, adapter: HeygenAdapter) -> None:
        self.adapter = adapter

    async def execute(self) -> list[IntegrationAvatarDTO]:
        response = await self.adapter.list_all_avatars()
        return [IntegrationAvatarDTO(**avatar.model_dump()) for avatar in response.data.avatars]
