from fastapi import APIRouter
from loguru import logger

from src.admin.api.dependencies import AdminAdapterDepend
from src.admin.domain.dtos import AppConnectDTO, AppTokenCreateDTO

router = APIRouter()


@router.post("/application")
async def application_connected(dto: AppConnectDTO, adapter: AdminAdapterDepend):
    logger.info(f"Application connected {dto}")
    await adapter.initialize()


@router.post("/token")
async def api_token_created(dto: AppTokenCreateDTO, adapter: AdminAdapterDepend):
    logger.info(f"Application token created {dto}")
    await adapter.initialize()
