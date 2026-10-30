from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class InventoryBase(BaseModel):
    quantity: Decimal = Field(default=Decimal("0.00"), ge=0)
    minimum_stock: Decimal = Field(default=Decimal("0.00"), ge=0)


class InventoryCreate(InventoryBase):
    product_id: int = Field(gt=0)


class InventoryUpdate(BaseModel):
    quantity: Decimal | None = Field(default=None, ge=0)
    minimum_stock: Decimal | None = Field(default=None, ge=0)


class InventoryResponse(InventoryBase):
    id: int
    product_id: int

    model_config = ConfigDict(from_attributes=True)