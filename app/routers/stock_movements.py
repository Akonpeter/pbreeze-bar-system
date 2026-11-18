from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_roles

from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse
)

#from app.services.stock_movement_service import create_stock_movement
from app.services.stock_movement_service import (
    create_stock_movement,
    get_all_stock_movements,
    get_stock_movement_by_id
)

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

# @router.get("/", response_model=list[StockMovementResponse])
# def read_stock_movements(
#     db: Session = Depends(get_db),
#     current_user=Depends(require_roles("admin", "manager"))
# ):
#     return get_all_stock_movements(db)

# @router.get("/", response_model=list[StockMovementResponse])
# def read_stock_movements(
#     product_id: int | None = None,
#     db: Session = Depends(get_db),
#     current_user=Depends(require_roles("admin", "manager"))
# ):
#     return get_all_stock_movements(db, product_id)

@router.get("/", response_model=list[StockMovementResponse])
def read_stock_movements(
    product_id: int | None = None,
    movement_type: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return get_all_stock_movements(
        db,
        product_id,
        movement_type
    )



@router.get("/{movement_id}", response_model=StockMovementResponse)
def read_stock_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return get_stock_movement_by_id(db, movement_id)