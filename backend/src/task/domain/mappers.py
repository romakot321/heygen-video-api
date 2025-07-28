import json

from src.integration.domain.dtos import IntegrationTaskResultDTO, IntegrationTaskStatus
from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskStatus


class IntegrationResponseToDomainMapper:
    def map_one(self, data: IntegrationTaskResultDTO) -> TaskResultDTO:
        return TaskResultDTO(
            external_task_id=data.external_task_id,
            status=self._map_status(data.status),
            result=self._map_result(data),
            error=data.error
        )

    def _map_result(self, data: IntegrationTaskResultDTO) -> str:
        return json.dumps({
            "thumbnail_url": data.thumbnail_url,
            "video_url": data.video_url,
        })

    def _map_status(self, status: IntegrationTaskStatus) -> TaskStatus:
        if status == IntegrationTaskStatus.waiting:
            return TaskStatus.queued
        elif status == IntegrationTaskStatus.pending:
            return TaskStatus.queued
        elif status == IntegrationTaskStatus.processing:
            return TaskStatus.started
        elif status == IntegrationTaskStatus.failed:
            return TaskStatus.failed
        elif status == IntegrationTaskStatus.completed:
            return TaskStatus.finished
        raise ValueError(f"Failed to map integration response: Unknown status {status}")
