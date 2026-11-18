
from pydantic import BaseModel, Field
from typing import List, Optional


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    payment_method: Optional[str] = None
    items: List[SaleItemCreate]


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    total_amount: float
    payment_method: Optional[str] = None
    status: str
    items: List[SaleItemResponse]

    class Config:
        from_attributes = True
