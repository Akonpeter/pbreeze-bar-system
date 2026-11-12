from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from typing import Literal


MovementType = Literal[
    "purchase",
    "sale",
    "damage",
    "adjustment"
]


class StockMovementCreate(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: Decimal = Field(gt=0)
    description: str | None = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: MovementType
    quantity: Decimal
    previous_quantity: Decimal
    new_quantity: Decimal
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
        