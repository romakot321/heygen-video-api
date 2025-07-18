from uuid import UUID

from src.admin.application.interfaces.repository import IAdminRepository


class GetCurrentApiIdUseCase:
    def __init__(self, repository: IAdminRepository):
        self.repository = repository

    async def execute(self) -> UUID:
        current_account = await self.repository.get_me()
        relations = await self.repository.get_account_entity_relations(current_account.id)

        api_relations = list(filter(lambda r: r.entity == "api", relations))
        if len(api_relations) == 0 or len(api_relations) > 1:
            raise ValueError(f"Unexpected relations list: {relations}")

        return UUID(api_relations[0].entity_id)