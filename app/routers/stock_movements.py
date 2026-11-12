from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_roles

from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse
)

from app.services.stock_movement_service import create_stock_movement


router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)


@router.post("/", response_model=StockMovementResponse)
def create_movement(
    movement_data: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return create_stock_movement(db, movement_data)