
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


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
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True




class SaleCancelRequest(BaseModel):
    reason: str = Field(
        min_length=3,
        max_length=500
    )