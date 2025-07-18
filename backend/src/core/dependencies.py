from typing import Optional

from fastapi import Header, HTTPException, Depends
from fastapi.security import APIKeyHeader
from loguru import logger

from src.admin.api.dependencies import get_admin_adapter
from src.admin.application.adapter import AdminAdapter
from src.admin.domain.exceptions import AdminException
from src.core.config import settings


class ApiTokenHeader(APIKeyHeader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name='api-token', **kwargs)

    @classmethod
    def check_api_key(cls, api_key: Optional[str], auto_error: bool) -> Optional[str]:
        api_key = super().check_api_key(api_key=api_key, auto_error=auto_error)
        return api_key


scheme = ApiTokenHeader()


async def validate_api_token(token: str = Depends(scheme), admin_adapter: AdminAdapter = Depends(get_admin_adapter)):
    try:
        await admin_adapter.authenticate_application(token)
    except AdminException as e:
        logger.error(e)
        raise HTTPException(403, detail="Not authenticated")
