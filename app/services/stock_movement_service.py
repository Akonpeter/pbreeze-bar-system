from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.inventory import Inventory
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementCreate



def create_stock_movement(
    db: Session,
    movement_data: StockMovementCreate
):
    # Find the product
    product = db.query(Product).filter(
        Product.id == movement_data.product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Find the product's inventory record
    inventory = db.query(Inventory).filter(
        Inventory.product_id == movement_data.product_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found"
        )




    previous_quantity = Decimal(str(inventory.quantity))
    movement_quantity = movement_data.quantity

    if movement_data.movement_type == "purchase":
        new_quantity = previous_quantity + movement_quantity

    elif movement_data.movement_type in ("sale", "damage"):
        new_quantity = previous_quantity - movement_quantity

    elif movement_data.movement_type == "adjustment":
        new_quantity = movement_quantity

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid movement type"
        )

    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )

    inventory.quantity = new_quantity

    stock_movement = StockMovement(
        product_id=movement_data.product_id,
        movement_type=movement_data.movement_type,
        quantity=movement_quantity,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        description=movement_data.description

    )

    db.add(stock_movement)
    db.commit()
    db.refresh(stock_movement)

    return stock_movement

    



# def get_all_stock_movements(db: Session):
#     stock_movements = db.query(StockMovement).order_by(
#         StockMovement.created_at.desc()
#     ).all()

#     return stock_movements

def get_all_stock_movements(
    db: Session,                      
    product_id: int | None = None,
     movement_type: str | None = None
    ):
    query = db.query(StockMovement)

    if product_id is not None:
        query = query.filter(StockMovement.product_id == product_id)


    if movement_type is not None:
        query = query.filter(
            StockMovement.movement_type == movement_type
    )


    stock_movements = query.order_by(
        StockMovement.created_at.desc()
    ).all()

    return stock_movements


def get_stock_movement_by_id(db: Session, movement_id: int):
    stock_movement = db.query(StockMovement).filter(
        StockMovement.id == movement_id
    ).first()

    if stock_movement is None:
        raise HTTPException(
            status_code=404,
            detail="Stock movement not found"
        )

    return stock_movement
