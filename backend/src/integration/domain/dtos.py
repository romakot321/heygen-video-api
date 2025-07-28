from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from src.integration.domain.schemas import HeygenRunRequest


class IntegrationTaskStatus(str, Enum):
    waiting = "waiting"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    pending = "pending"


class IntegrationTaskRunParamsDTO(HeygenRunRequest):
    pass


class IntegrationTaskResultDTO(BaseModel):
    status: IntegrationTaskStatus
    external_task_id: str | None = None
    thumbnail_url: str | None = None
    video_url: str | None = None
    error: str | None = None


class IntegrationAvatarDTO(BaseModel):
    avatar_id: str
    avatar_name: str
    preview_image_url: str
    preview_video_url: str
    gender: str
    premium: bool


class IntegrationVoiceDTO(BaseModel):
    voice_id: str
    language: str
    gender: str
    name: str
    preview_audio: str
    support_pause: bool
    emotion_support: bool
    support_locale: bool


class AvatarCreateDTO(BaseModel):
    user_id: str
    app_bundle: str


class AvatarReadDTO(BaseModel):
    id: UUID
    user_id: str
    app_bundle: str
    heygen_id: str | None = None


class HeygenBackgroundDTO(BaseModel):
    url: str
