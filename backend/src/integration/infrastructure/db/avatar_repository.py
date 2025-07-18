from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelConflictException, DBModelNotFoundException
from src.integration.application.interfaces.avatar_repository import IAvatarRepository
from src.integration.domain.entities import AvatarCreate, Avatar, AvatarUpdate
from src.integration.infrastructure.db.orm import AvatarDB


class PGAvatarRepository(IAvatarRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e)
            raise DBModelConflictException(detail)

    async def create(self, data: AvatarCreate) -> Avatar:
        model = AvatarDB(**data.model_dump())
        self.session.add()
        await self._flush()
        return self._to_domain(model)

    async def get_list_by_user(self, user_id: str, app_bundle: str) -> list[Avatar]:
        query = select(AvatarDB).filter_by(user_id=user_id, app_bundle=app_bundle)
        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    async def update_by_pk(self, pk: UUID, data: AvatarUpdate) -> None:
        query = update(AvatarDB).where(AvatarDB.id == pk).values(**data.model_dump(exclude_unset=True))
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise DBModelNotFoundException()
        await self._flush()

    @staticmethod
    def _to_domain(model: AvatarDB) -> Avatar:
        return Avatar.model_validate(model)