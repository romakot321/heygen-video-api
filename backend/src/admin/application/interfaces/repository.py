import abc
from uuid import UUID

from src.admin.domain.entities import ApiConnection, Account, AccountEntityRelation, Product, User, \
    ProductPurchaseCreate, ProductPurchase, App


class IAdminRepository(abc.ABC):
    @abc.abstractmethod
    async def get_connections(self, api_id: UUID) -> list[ApiConnection]: ...

    @abc.abstractmethod
    async def get_me(self) -> Account: ...

    @abc.abstractmethod
    async def get_account_entity_relations(self, account_id: int) -> list[AccountEntityRelation]: ...

    @abc.abstractmethod
    async def get_app_products_list(self, app_id: UUID) -> list[Product]: ...

    @abc.abstractmethod
    async def get_user(self, apphud_id: str, app_id: UUID) -> User: ...

    @abc.abstractmethod
    async def create_product_purchase(self, data: ProductPurchaseCreate) -> ProductPurchase: ...

    @abc.abstractmethod
    async def get_app_by_id(self, app_id: UUID) -> App: ...