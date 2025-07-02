from loguru import logger

from src.core.config import settings
from src.core.http.client import IHttpClient
from src.integration.domain.schemas import HeygenRunResponse, HeygenRunRequest, HeygenStatusResponse, \
    HeygenAvatarsResponse, HeygenVoicesResponse
from src.integration.infrastructure.http_api_client import HttpApiClient


class HeygenAdapter(HttpApiClient):
    token: str = settings.HEYGEN_API_TOKEN
    api_url: str = "https://api.heygen.com"

    def __init__(self, client: IHttpClient) -> None:
        super().__init__(client=client, source_url=self.api_url, token=self.token)

    async def create_avatar_video(self, request: HeygenRunRequest) -> HeygenRunResponse:
        await self.check_account_balance()
        response = await self.request("POST", "/v2/video/generate", json=request.model_dump(exclude_none=True))
        return self.validate_response(response.data, HeygenRunResponse)

    async def retrieve_video_status(self, video_id: str) -> HeygenStatusResponse:
        response = await self.request("GET", "/v1/video_status.get", params={"video_id": video_id})
        return self.validate_response(response.data, HeygenStatusResponse)

    async def check_account_balance(self):
        response = await self.request("GET", "/v2/user/remaining_quota")
        if response.data.get("remaining_quota", 0) // 60 <= 10:
            logger.bind(name="balance").error(
                f"Heygen account balance is low: {response.data.get('remaining_quota', 0) // 60} credits")

    async def list_all_avatars(self) -> HeygenAvatarsResponse:
        response = await self.request("GET", "/v2/avatars")
        return self.validate_response(response.data, HeygenAvatarsResponse)

    async def list_all_voices(self) -> HeygenVoicesResponse:
        response = await self.request("GET", "/v2/voices")
        return self.validate_response(response.data, HeygenVoicesResponse)
