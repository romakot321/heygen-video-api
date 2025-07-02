import os

from src.admin.application.adapter import AdminAdapter
from src.admin.application.interfaces.admin_data_storage import IAdminDataStorage
from src.admin.application.interfaces.repository import IAdminRepository
from src.admin.infrastructure.http.client import AsyncHttpClient
from src.admin.infrastructure.http.repository import HttpAdminRepository
from src.admin.infrastructure.inmemory_admin_data_storage import InMemoryAdminDataStorage


def get_admin_repository() -> IAdminRepository:
    access_token = os.getenv("ADMINPANEL_API_ACCESS_TOKEN")
    if access_token is None:
        raise ValueError("Can't initialize admin repository: Empty ADMINPANEL_API_ACCESS_TOKEN")

    source_url = os.getenv("ADMINPANEL_API_BASE_URL")
    if source_url is None:
        raise ValueError("Can't initialize admin repository: Empty ADMINPANEL_API_BASE_URL")

    return HttpAdminRepository(access_token, AsyncHttpClient(), source_url)


def get_admin_data_storage() -> IAdminDataStorage:
    return InMemoryAdminDataStorage()


def get_admin_adapter() -> AdminAdapter:
    repository = get_admin_repository()
    storage = get_admin_data_storage()
    return AdminAdapter(repository, storage)