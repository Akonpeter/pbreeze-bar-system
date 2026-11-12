from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.auth.dependencies import get_current_user, require_roles


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)




@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_inventory(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    # Check whether the product exists.
    product = db.query(Product).filter(
        Product.id == inventory_data.product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check whether inventory already exists for this product.
    existing_inventory = db.query(Inventory).filter(
        Inventory.product_id == inventory_data.product_id
    ).first()

    if existing_inventory:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inventory already exists for this product"
        )

    # Create the inventory record.
    new_inventory = Inventory(
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity,
        minimum_stock=inventory_data.minimum_stock
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory



@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def list_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    inventory_items = db.query(Inventory).order_by(
        Inventory.id
    ).all()

    return inventory_items



@router.get("/low-stock", response_model=list[InventoryResponse])
def get_low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    low_stock_items = db.query(Inventory).filter(
        Inventory.quantity <= Inventory.minimum_stock
    ).all()

    return low_stock_items



@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse
)
def get_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    inventory_item = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found"
        )

    return inventory_item




@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    inventory_item = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found"
        )

    update_data = inventory_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(inventory_item, field, value)

    db.commit()
    db.refresh(inventory_item)

    return inventory_item



@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    inventory_item = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found"
        )

    db.delete(inventory_item)
    db.commit()

    return {
        "message": "Inventory record deleted successfully"
    }

