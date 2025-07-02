from src.integration.domain.dtos import IntegrationVoiceDTO
from src.integration.infrastructure.adapter import HeygenAdapter


class GetVoicesUseCase:
    def __init__(self, adapter: HeygenAdapter) -> None:
        self.adapter = adapter

    async def execute(self) -> list[IntegrationVoiceDTO]:
        response = await self.adapter.list_all_voices()
        return [IntegrationVoiceDTO(**avatar.model_dump()) for avatar in response.voices]
