from src.integration.application.interfaces.avatar_uow import IAvatarUnitOfWork
from src.integration.domain.dtos import AvatarReadDTO
from src.integration.domain.entities import AvatarUpdate
from src.integration.infrastructure.adapter import HeygenAdapter


class GetUserAvatarsListUseCase:
    def __init__(self, uow: IAvatarUnitOfWork, heygen_adapter: HeygenAdapter):
        self.uow = uow
        self.heygen_adapter = heygen_adapter

    async def execute(self, user_id: str, app_bundle: str) -> list[AvatarReadDTO]:
        async with self.uow:
            avatars = await self.uow.avatars.get_list_by_user(user_id, app_bundle)

            for avatar in avatars:
                if avatar.heygen_id:
                    continue
                train_status = await self.heygen_adapter.get_train_photo_avatar_group_status(avatar.heygen_group_id)
                if train_status.data.status == "pending":
                    continue
                await self.uow.avatars.update_by_pk(avatar.id, AvatarUpdate(heygen_id=avatar.heygen_group_id))
                avatar.heygen_id = avatar.heygen_group_id

            await self.uow.commit()

        return [AvatarReadDTO(**avatar.model_dump()) for avatar in avatars]