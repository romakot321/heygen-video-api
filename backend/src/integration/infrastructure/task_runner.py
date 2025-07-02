import json

from src.core.config import settings
from src.integration.domain.dtos import IntegrationTaskResultDTO, IntegrationTaskStatus
from src.integration.domain.mappers import TaskRunToRequestMapper
from src.integration.infrastructure.adapter import HeygenAdapter
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.domain.entities import TaskRun


class HeygenTaskRunner(ITaskRunner[IntegrationTaskResultDTO]):
    token: str = settings.HEYGEN_API_TOKEN
    api_url: str = ""

    def __init__(self, adapter: HeygenAdapter) -> None:
        self.adapter = adapter

    async def start(self, data: TaskRun) -> IntegrationTaskResultDTO:
        request = TaskRunToRequestMapper().map_one(data)
        response = await self.adapter.create_avatar_video(request)
        response = response.data
        return IntegrationTaskResultDTO(status=IntegrationTaskStatus.pending, external_task_id=response.video_id)

    async def get_result(self, external_task_id: str) -> IntegrationTaskResultDTO | None:
        response = await self.adapter.retrieve_video_status(external_task_id)
        response = response.data
        error = None if response.error is None else json.dumps(response.error)
        return IntegrationTaskResultDTO(status=response.status, external_task_id=external_task_id,
                                        thumbnail_url=response.thumbnail_url, video_url=response.video_url, error=error)
