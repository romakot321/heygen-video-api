from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ApiConnection(BaseModel):
    id: int
    app_id: UUID
    api_id: UUID
    api_token: str


class Account(BaseModel):
    id: int
    name: str
    attributes: list[str]


class AccountEntityRelation(BaseModel):
    account_id: int
    entity: str
    entity_id: str
    relation_type: str


class Product(BaseModel):
    id: UUID
    name: str
    tokens_amount: int


class ProductPurchaseCreate(BaseModel):
    product_id: UUID
    user_id: UUID
    app_id: UUID


class ProductPurchase(BaseModel):
    apphud_product_id: str | None = None
    apphud_transaction_id: str | None = None
    apphud_app_bundle: str | None = None
    apphud_user_id: str | None = None
    product_id: UUID | None = None
    user_id: UUID | None =  None
    app_id: UUID | None = None


class User(BaseModel):
    id: UUID
    apphud_id: str
    app_id: UUID


class App(BaseModel):
    id: UUID
    name: str
    bundle: str