from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from src.integration.domain.dtos import IntegrationTaskRunParamsDTO


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    failed = "failed"
    finished = "finished"


class Task(BaseModel):
    id: UUID
    user_id: str
    app_bundle: str
    status: TaskStatus
    result: str | None = None
    error: str | None = None


class TaskCreate(BaseModel):
    user_id: str
    app_bundle: str


class TaskResultQuality(str, Enum):
    draft = 'draft'
    low = 'low'
    medium = 'medium'
    high = 'high'
    premium = 'premium'


class TaskRun(IntegrationTaskRunParamsDTO, BaseModel):
    pass


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    result: str | None = None
    error: str | None = None
