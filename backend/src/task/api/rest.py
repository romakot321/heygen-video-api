from uuid import UUID

from fastapi import Depends, APIRouter, BackgroundTasks

from src.task.api.dependencies import HttpClientDepend, TaskUoWDepend, TaskRunnerDepend
from src.task.application.use_cases.create_task import CreateTaskUseCase
from src.task.application.use_cases.get_task import GetTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO

router = APIRouter()


@router.post("", response_model=TaskReadDTO)
async def create_and_run_task(
        uow: TaskUoWDepend,
        http_client: HttpClientDepend,
        runner: TaskRunnerDepend,
        background_tasks: BackgroundTasks,
        data: TaskCreateDTO,
):
    task = await CreateTaskUseCase(uow).execute(data)
    background_tasks.add_task(RunTaskUseCase(uow, runner, http_client).execute, task.id, data)
    return task


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: UUID, uow: TaskUoWDepend):
    return await GetTaskUseCase(uow).execute(task_id)
