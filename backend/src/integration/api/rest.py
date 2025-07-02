from fastapi import APIRouter

from src.integration.api.dependencies import HeygenAdapterDepend
from src.integration.application.use_cases.get_avatars import GetAvatarsUseCase
from src.integration.application.use_cases.get_voices import GetVoicesUseCase
from src.integration.domain.dtos import IntegrationAvatarDTO, IntegrationVoiceDTO

router = APIRouter()


@router.get("/heygen/avatars", response_model=list[IntegrationAvatarDTO])
async def get_heygen_avatars(adapter: HeygenAdapterDepend):
    return await GetAvatarsUseCase(adapter).execute()


@router.get("/heygen/voices", response_model=list[IntegrationVoiceDTO])
async def get_heygen_voices(adapter: HeygenAdapterDepend):
    return await GetVoicesUseCase(adapter).execute()
