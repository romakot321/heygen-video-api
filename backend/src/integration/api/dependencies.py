from typing import Annotated

from fastapi import Depends

from src.core.http.client import AsyncHttpClient
from src.integration.infrastructure.adapter import HeygenAdapter
from src.integration.infrastructure.task_runner import HeygenTaskRunner
from src.task.application.interfaces.task_runner import ITaskRunner


def get_heygen_adapter() -> HeygenAdapter:
    return HeygenAdapter(AsyncHttpClient())


def get_integration_task_runner() -> ITaskRunner:
    adapter = get_heygen_adapter()
    return HeygenTaskRunner(adapter)


HeygenAdapterDepend = Annotated[HeygenAdapter, Depends(get_heygen_adapter)]
