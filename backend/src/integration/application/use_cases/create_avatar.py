from io import BytesIO
import random

from fastapi import HTTPException
from loguru import logger

from src.integration.application.interfaces.avatar_uow import IAvatarUnitOfWork
from src.integration.domain.dtos import AvatarCreateDTO, AvatarReadDTO
from src.integration.domain.entities import AvatarCreate, Avatar
from src.integration.domain.schemas import HeygenCreatePhotoAvatarGroupRequest, HeygenAddLooksToPhotoAvatarGroupRequest
from src.integration.infrastructure.adapter import HeygenAdapter
from src.integration.domain.exceptions import IntegrationRequestException


class CreateAvatarUseCase:
    def __init__(self, uow: IAvatarUnitOfWork, heygen_adapter: HeygenAdapter) -> None:
        self.uow = uow
        self.heygen_adapter = heygen_adapter

    async def execute(self, dto: AvatarCreateDTO, images: list[BytesIO]) -> AvatarReadDTO:
        if not images:
            raise HTTPException(422, detail="Must be at least one image")
        images_keys = await self._upload_images(images)
        group_response = await self._create_group(dto, images_keys)
        await self._train(group_response.data.group_id)
        avatar = await self._create_entity(dto, group_response.data.group_id)
        return AvatarReadDTO(**avatar.model_dump())

    async def _train(self, heygen_group_id: str):
        for second in range(61):
            response = await self.heygen_adapter.list_all_avatars_in_one_avatar_group(heygen_group_id)
            if all([a.status == "completed" for a in response.data.avatar_list]):
                break
            if second == 59:
                raise HTTPException(500, detail="Timeout for group creating")

        try:
            await self.heygen_adapter.train_photo_avatar_group(heygen_group_id)
        except IntegrationRequestException as e:
            raise HTTPException(400, detail=str(e.message))

    async def _upload_images(self, images: list[BytesIO]) -> list[str]:
        images_keys = []
        for image in images:
            response = await self.heygen_adapter.upload_asset(image)
            images_keys.append(response.data.image_key)
        return images_keys

    async def _create_group(self, dto: AvatarCreateDTO, images_keys: list[str]):
        group_name = f"{dto.user_id}:{dto.app_bundle}:{random.randint(0, 100)}"
        group_response = await self.heygen_adapter.create_photo_avatar_group(HeygenCreatePhotoAvatarGroupRequest(name=group_name, image_key=images_keys[0]))
        if len(images_keys) > 1:
            await self.heygen_adapter.add_looks_to_photo_avatar_group(HeygenAddLooksToPhotoAvatarGroupRequest(group_id=group_response.data.group_id, image_keys=images_keys[1:], name=group_name + "Look"))
        logger.info(f"Created group {group_name=} with id={group_response.data.group_id}")
        return group_response

    async def _create_entity(self, dto: AvatarCreateDTO, heygen_group_id: str) -> Avatar:
        command = AvatarCreate(**dto.model_dump(), heygen_group_id=heygen_group_id)
        async with self.uow:
            avatar = await self.uow.avatars.create(command)
            await self.uow.commit()
        return avatar
