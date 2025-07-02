from uuid import UUID

from pydantic import BaseModel


class AppConnectDTO(BaseModel):
    application_id: str


class AppTokenCreateDTO(BaseModel):
    application_id: str
    token: str


class ApiConnectionReadDTO(BaseModel):
    app_id: UUID
    app_bundle: str
    api_token: str
