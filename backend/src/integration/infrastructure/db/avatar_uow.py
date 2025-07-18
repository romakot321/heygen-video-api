from src.db.engine import async_session_maker
from src.integration.application.interfaces.avatar_uow import IAvatarUnitOfWork
from src.integration.infrastructure.db.avatar_repository import PGAvatarRepository


class PGAvatarUnitOfWork(IAvatarUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.avatars = PGAvatarRepository(self.session)
        return await super().__aenter__()

    async def commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()