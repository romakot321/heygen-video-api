from fastapi import FastAPI

from src.admin.api.rest import router as admin_router


def setup_admin_integration(app: FastAPI):
    admin_app = FastAPI()
    admin_app.include_router(admin_router, include_in_schema=False)

    app.mount("/api/admin", admin_app)

