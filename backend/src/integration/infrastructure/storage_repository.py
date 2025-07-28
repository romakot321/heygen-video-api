import uuid
from pathlib import Path


class StorageRepository:
    path = Path("storage")

    def write(self, file_body: bytes) -> str:
        filename = uuid.uuid4().hex
        with open(self.path / filename, "wb") as f:
            f.write(file_body)
        return filename

    def read(self, filename: str) -> bytes:
        with open(self.path / filename, "rb") as f:
            return f.read()