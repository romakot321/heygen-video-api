from src.integration.domain.schemas import HeygenRunRequest
from src.task.domain.entities import TaskRun


class TaskRunToRequestMapper:
    def map_one(self, task_run: TaskRun) -> HeygenRunRequest:
        return HeygenRunRequest(**task_run.model_dump())
