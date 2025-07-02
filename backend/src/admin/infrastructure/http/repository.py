from uuid import UUID

from src.admin.application.interfaces.http_client import IHttpClient
from src.admin.application.interfaces.repository import IAdminRepository
from src.admin.domain.entities import App, ProductPurchaseCreate, ProductPurchase, User, Product, AccountEntityRelation, \
    Account, ApiConnection
from src.admin.domain.exceptions import AdminException
from src.admin.infrastructure.http.http_api_client import HttpApiClient


class HttpAdminRepository(HttpApiClient, IAdminRepository):
    def __init__(self, access_token: str, client: IHttpClient, source_url: str):
        super().__init__(client, source_url, token=access_token)

    async def get_connections(self, api_id: UUID) -> list[ApiConnection]:
        response = await self.request("GET", f"/backend/api/{api_id}/connections", params={"limit": 10000})

        if not isinstance(response.data, list):
            raise AdminException(f"Unexpected response: {response}")
        return [self.validate_response(i, ApiConnection) for i in response.data]

    async def get_me(self) -> Account:
        response = await self.request("GET", "/backend/auth/me")
        return self.validate_response(response.data, Account)

    async def get_account_entity_relations(self, account_id: int) -> list[AccountEntityRelation]:
        response = await self.request("GET", f"/backend/account/{account_id}/relation")

        if not isinstance(response.data, list):
            raise AdminException(f"Unexpected response: {response}")
        return [self.validate_response(i, AccountEntityRelation) for i in response.data]

    async def get_app_products_list(self, app_id: UUID) -> list[Product]:
        response = await self.request("GET", "/backend/product", params={"limit": 10000, "app_id": app_id})

        if not isinstance(response.data, list):
            raise AdminException(f"Unexpected response: {response}")
        return [self.validate_response(i, Product) for i in response.data]

    async def get_user(self, apphud_id: str, app_id: UUID) -> User:
        response = await self.request("GET", "/backend/user/apphud", params={"apphud_id": apphud_id, "app_id": app_id})
        return self.validate_response(response.data, User)

    async def create_product_purchase(self, data: ProductPurchaseCreate) -> ProductPurchase:
        response = await self.request("POST", "/backend/product/purchase", json=data.model_dump())
        return self.validate_response(response.data, ProductPurchase)

    async def get_app_by_id(self, app_id: UUID) -> App:
        response = await self.request("GET", f"/backend/app/{app_id}")
        return self.validate_response(response.data, App)