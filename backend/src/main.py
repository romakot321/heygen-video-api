from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from src.admin.api.dependencies import get_admin_adapter
from src.admin.main import setup_admin_integration
from src.core.dependencies import validate_api_token
from src.core.logging_setup import setup_fastapi_logging
from src.integration.api.rest import router as integration_router
from src.task.api.rest import router as task_router


@asynccontextmanager
async def lifespan(app):
    await get_admin_adapter().initialize()
    yield


app = FastAPI(title="heygen video api", dependencies=[Depends(validate_api_token)], lifespan=lifespan)
setup_fastapi_logging(app)
setup_admin_integration(app)

app.include_router(task_router, tags=["Task"], prefix="/api/task")
app.include_router(integration_router, tags=["Integration"], prefix="/api/integration")
