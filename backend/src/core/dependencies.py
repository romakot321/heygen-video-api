from typing import Optional

from fastapi import Header, HTTPException, Depends
from fastapi.security import APIKeyHeader

from src.core.config import settings


class ApiTokenHeader(APIKeyHeader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name='api-token', **kwargs)

    @classmethod
    def check_api_key(cls, api_key: Optional[str], auto_error: bool) -> Optional[str]:
        api_key = super().check_api_key(api_key=api_key, auto_error=auto_error)
        if api_key != settings.API_TOKEN:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return api_key


scheme = ApiTokenHeader()


def validate_api_token(token: str = Depends(scheme)):
    pass
