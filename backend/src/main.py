from fastapi import FastAPI, Depends

from src.core.dependencies import validate_api_token
from src.core.logging_setup import setup_fastapi_logging
from src.integration.api.rest import router as integration_router
from src.task.api.rest import router as task_router

app = FastAPI(title="heygen video api", dependencies=[Depends(validate_api_token)])
setup_fastapi_logging(app)

app.include_router(task_router, tags=["Task"], prefix="/api/task")
app.include_router(integration_router, tags=["Integration"], prefix="/api/integration")
