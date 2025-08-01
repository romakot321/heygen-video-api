from io import BytesIO

from loguru import logger

from src.core.config import settings
from src.core.http.client import IHttpClient
from src.integration.domain.schemas import HeygenRunResponse, HeygenRunRequest, HeygenStatusResponse, \
    HeygenAvatarsResponse, HeygenVoicesResponse, HeygenAssetUploadResponse, HeygenCreatePhotoAvatarGroupRequest, \
    HeygenCreatePhotoAvatarGroupResponse, HeygenAddLooksToPhotoAvatarGroupRequest, HeygenGetTrainingJobStatusResponse, \
    HeygenAvatarsInGroupResponse
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

    async def upload_asset(self, file: BytesIO, content_type: str) -> HeygenAssetUploadResponse:
        if content_type.endswith("jpeg"):
            file.name = "tmp.jpeg"
        else:
            file.name = "tmp.jpeg"
        response = await self.request("POST", "https://upload.heygen.com/v1/asset", data=file)
        return self.validate_response(response.data, HeygenAssetUploadResponse)

    async def create_photo_avatar_group(self, request: HeygenCreatePhotoAvatarGroupRequest) -> HeygenCreatePhotoAvatarGroupResponse:
        response = await self.request("POST", "/v2/photo_avatar/avatar_group/create", json=request.model_dump())
        return self.validate_response(response.data, HeygenCreatePhotoAvatarGroupResponse)

    async def add_looks_to_photo_avatar_group(self, request: HeygenAddLooksToPhotoAvatarGroupRequest):
        response = await self.request("POST", "/v2/photo_avatar/avatar_group/add", json=request.model_dump())

    async def train_photo_avatar_group(self, group_id: str):
        await self.request("POST", "/v2/photo_avatar/train", json={"group_id": group_id})

    async def get_train_photo_avatar_group_status(self, group_id: str) -> HeygenGetTrainingJobStatusResponse:
        response = await self.request("GET", f"/v2/photo_avatar/train/status/{group_id}")
        return self.validate_response(response.data, HeygenGetTrainingJobStatusResponse)

    async def list_all_avatars_in_one_avatar_group(self, group_id: str) -> HeygenAvatarsInGroupResponse:
        response = await self.request("GET", f"/v2/avatar_group/{group_id}/avatars")
        return self.validate_response(response.data, HeygenAvatarsInGroupResponse)
