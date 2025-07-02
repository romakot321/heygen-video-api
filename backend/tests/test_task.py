import types
from io import BytesIO
from typing import Type, Literal, get_args
from httpx import AsyncClient
from pydantic import BaseModel
import pytest

from src.core.config import settings
from src.task.domain.dtos import TaskCreateDTO
from src.task.domain.entities import TaskStatus


def _fill_dto(dto: Type[BaseModel]) -> dict:
    data = {}
    for name, field in dto.model_fields.items():
        if isinstance(field.annotation, types.UnionType):
            field.annotation = field.annotation.__args__[-1]

        if field.annotation is str:
            data[name] = "string"
        elif field.annotation is list:
            data[name] = []
        elif field.annotation is int:
            data[name] = 0
        elif field.annotation is float:
            data[name] = 1.0
        elif hasattr(field.annotation, "model_validate"):
            data[name] = _fill_dto(field.annotation)
        else:
            data[name] = None
    return data


@pytest.mark.asyncio(loop_scope="session")
async def test_task_create(test_client: AsyncClient):
    data = _fill_dto(TaskCreateDTO)
    data['voice']['type'] = "silence"

    resp = await test_client.post("/api/task", json=data, headers={"Api-Token": settings.API_TOKEN})
    assert resp.status_code == 200, resp.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_task_get(test_client: AsyncClient):
    data = _fill_dto(TaskCreateDTO)
    data['voice']['type'] = "silence"

    resp = await test_client.post("/api/task", json=data, headers={"Api-Token": settings.API_TOKEN})
    assert resp.status_code == 200, resp.json()
    task_id = resp.json()["id"]

    resp = await test_client.get(f"/api/task/{task_id}", headers={"Api-Token": settings.API_TOKEN})
    assert resp.status_code == 200, resp.json()
    assert resp.json() == dict(id=task_id, status=TaskStatus.finished, result='{"thumbnail_url": "a", "video_url": "a"}', error=None)