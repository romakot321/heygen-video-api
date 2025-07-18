import json
from uuid import UUID

from fastapi import HTTPException

from src.db.exceptions import DBModelNotFoundException
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO


class GetTaskUseCase:
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def execute(self, task_id: UUID) -> TaskReadDTO:
        async with self.uow:
            try:
                task = await self.uow.tasks.get_by_pk(task_id)
            except DBModelNotFoundException:
                raise HTTPException(404)
        result = json.loads(task.result) if task.result else {"thumbnail_url": None, "video_url": None}
        return TaskReadDTO(**task.model_dump(exclude={"result"}), **result)
