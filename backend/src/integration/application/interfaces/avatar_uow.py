import abc

from src.integration.application.interfaces.avatar_repository import IAvatarRepository


class IAvatarUnitOfWork(abc.ABC):
    avatars: IAvatarRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._rollback()

    @abc.abstractmethod
    async def commit(self): ...

    @abc.abstractmethod
    async def _rollback(self): ...