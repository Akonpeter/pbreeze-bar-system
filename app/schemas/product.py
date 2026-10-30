from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict



class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, Max_length=500)
    sku: str | None = Field(default=None, max_length=100)
    cost_price: Decimal = Field(default=Decimal("0.00"), ge=0)
    selling_price: Decimal = Field(gt=0)
    category_id: int = Field(gt=0)

class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    sku: str | None = Field(default=None, max_length=100)
    cost_price: Decimal | None = Field(default=None, gt=0)
    selling_price: Decimal | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    