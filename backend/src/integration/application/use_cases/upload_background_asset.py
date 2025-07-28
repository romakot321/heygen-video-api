from fastapi import UploadFile

from src.core.config import settings
from src.integration.domain.dtos import HeygenBackgroundDTO
from src.integration.infrastructure.storage_repository import StorageRepository


class UploadBackgroundAssetUseCase:
    def __init__(self, storage: StorageRepository):
        self.storage = storage

    def execute(self, file: UploadFile) -> HeygenBackgroundDTO:
        filename = self.storage.write(file.file.read())
        return HeygenBackgroundDTO(url="https://" + settings.DOMAIN + "/api/storage/" + filename)