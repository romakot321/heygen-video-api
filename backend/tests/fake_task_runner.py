from io import BytesIO

from src.integration.domain.dtos import IntegrationTaskResultDTO, IntegrationTaskStatus
from src.integration.domain.schemas import HeygenRunResponse
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.domain.entities import TaskRun


class FakeTaskRunner(ITaskRunner):
    def __init__(self):
        self.tasks = []

    async def start(self, data: TaskRun) -> IntegrationTaskResultDTO:
        self.tasks.append(data)
        return IntegrationTaskResultDTO(status=IntegrationTaskStatus.pending, external_task_id=str(len(self.tasks) - 1))

    async def get_result(self, external_task_id: str) -> IntegrationTaskResultDTO | None:
        return IntegrationTaskResultDTO(status=IntegrationTaskStatus.completed, external_task_id=external_task_id, thumbnail_url="a", video_url="a")