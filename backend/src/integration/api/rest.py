from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, Query

from src.integration.api.dependencies import HeygenAdapterDepend, AvatarUoWDepend, StorageRepositoryDepend
from src.integration.application.use_cases.create_avatar import CreateAvatarUseCase
from src.integration.application.use_cases.get_avatars import GetAvatarsUseCase
from src.integration.application.use_cases.get_user_avatars_list import GetUserAvatarsListUseCase
from src.integration.application.use_cases.get_voices import GetVoicesUseCase
from src.integration.application.use_cases.upload_background_asset import UploadBackgroundAssetUseCase
from src.integration.domain.dtos import IntegrationAvatarDTO, IntegrationVoiceDTO, AvatarReadDTO, AvatarCreateDTO, \
    HeygenBackgroundDTO

router = APIRouter()


@router.get("/heygen/avatars", response_model=list[IntegrationAvatarDTO])
async def get_heygen_avatars(adapter: HeygenAdapterDepend):
    return await GetAvatarsUseCase(adapter).execute()


@router.get("/heygen/voices", response_model=list[IntegrationVoiceDTO])
async def get_heygen_voices(adapter: HeygenAdapterDepend):
    return await GetVoicesUseCase(adapter).execute()


@router.post("/heygen/avatar", response_model=AvatarReadDTO)
async def create_user_heygen_avatar(adapter: HeygenAdapterDepend, uow: AvatarUoWDepend, images: list[UploadFile], dto: AvatarCreateDTO = Depends()):
    images = [(BytesIO(await image.read()), image.content_type) for image in images]
    return await CreateAvatarUseCase(uow, adapter).execute(dto, images)


@router.get("/heygen/avatar", response_model=list[AvatarReadDTO])
async def get_user_heygen_avatars_list(uow: AvatarUoWDepend, adapter: HeygenAdapterDepend, user_id: str = Query(), app_bundle: str = Query()):
    return await GetUserAvatarsListUseCase(uow, adapter).execute(user_id, app_bundle)


@router.post("/heygen/background", response_model=HeygenBackgroundDTO)
def upload_background_asset(storage: StorageRepositoryDepend, file: UploadFile):
    return UploadBackgroundAssetUseCase(storage).execute(file)