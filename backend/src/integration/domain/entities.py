from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Avatar(BaseModel):
    id: UUID
    user_id: str
    app_bundle: str
    heygen_id: str | None = None
    heygen_group_id: str

    model_config = ConfigDict(from_attributes=True)


class AvatarCreate(BaseModel):
    user_id: str
    app_bundle: str
    heygen_id: str | None = None
    heygen_group_id: str


class AvatarUpdate(BaseModel):
    heygen_id: str | None = None
