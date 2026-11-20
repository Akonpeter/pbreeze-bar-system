from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.stock_movement import StockMovement
from app.schemas.sale import SaleCreate, SaleCancelRequest
from datetime import datetime, timezone



def create_sale(db: Session, sale_data: SaleCreate):
    # Start with an empty list of validated sale items.
    validated_items = []

    # Keep track of the total sale amount.
    total_amount = Decimal("0.00")

    # Prevent the same product from appearing twice in one sale.
    product_ids = [
        item.product_id for item in sale_data.items
    ]

    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product can only appear once in a sale."
        )

    try:
        # Validate every product and its available inventory.
        for item in sale_data.items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found."
                )

            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            if inventory is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Inventory for {product.name} not found."
                )

            requested_quantity = Decimal(item.quantity)

            if inventory.quantity < requested_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.name}."
                )

            # Get the selling price from the database.
            unit_price = Decimal(product.selling_price)

            # Calculate the subtotal.
            subtotal = unit_price * requested_quantity

            total_amount += subtotal

            validated_items.append({
                "product": product,
                "inventory": inventory,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
            })

        

                # Do not allow an empty sale.
        if not validated_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sale must contain at least one product."
            )

        # Create the main sale record.
        sale = Sale(
            total_amount=total_amount,
            payment_method=sale_data.payment_method,
            status="completed"
        )

        db.add(sale)

        # Generate the sale ID before creating sale items.
        db.flush()

        # Process each validated product.
        for item in validated_items:

            inventory = item["inventory"]
            quantity_sold = Decimal(item["quantity"])

            # Record the stock before deduction.
            previous_quantity = Decimal(inventory.quantity)

            # Calculate the remaining stock.
            new_quantity = previous_quantity - quantity_sold

            # Update inventory.
            inventory.quantity = new_quantity

            # Create the sale item.
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                subtotal=item["subtotal"]
            )

            db.add(sale_item)

            # Record the stock movement.
            movement = StockMovement(
                product_id=item["product"].id,
                movement_type="sale",
                quantity=quantity_sold,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                description=f"Product sold in Sale #{sale.id}"
            )

            db.add(movement)

        # Save all changes together.
        db.commit()

        # Refresh the sale record from the database.
        db.refresh(sale)

        return sale

    except Exception:
        db.rollback()
        raise




def get_all_sales(db: Session):
    """
    Retrieve all recorded sales from the database.
    """

    sales = db.query(Sale).order_by(
        Sale.created_at.desc()
    ).all()

    return sales






def get_sale_by_id(db: Session, sale_id: int):
    """
    Retrieve a single sale using its ID.
    """

    sale = db.query(Sale).filter(
        Sale.id == sale_id
    ).first()

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found."
        )

    return sale


def cancel_sale(
    db: Session,
    sale_id: int,
    cancellation_data: SaleCancelRequest
):
    try:
        # Lock the sale to prevent simultaneous cancellations.
        sale = db.query(Sale).filter(
            Sale.id == sale_id
        ).with_for_update().first()

        if sale is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found."
            )

        # Prevent cancelling a sale more than once.
        if sale.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This sale has already been cancelled."
            )

        # Only completed sales can be cancelled.
        if sale.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only completed sales can be cancelled."
            )

        # Validate the cancellation reason.
        reason = cancellation_data.reason.strip()

        if len(reason) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide a valid cancellation reason."
            )

        # Retrieve sale items in a consistent order.
        sale_items = db.query(SaleItem).filter(
            SaleItem.sale_id == sale.id
        ).order_by(SaleItem.product_id).all()

        if not sale_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This sale has no items to restore."
            )

        # Restore each product's sold quantity.
        for item in sale_items:

            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            if inventory is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Inventory for product "
                        f"{item.product_id} not found."
                    )
                )

            previous_quantity = Decimal(
                str(inventory.quantity)
            )

            quantity_to_restore = Decimal(
                str(item.quantity)
            )

            new_quantity = (
                previous_quantity + quantity_to_restore
            )

            # Restore inventory.
            inventory.quantity = new_quantity

            # Record the cancellation stock movement.
            movement = StockMovement(
                product_id=item.product_id,
                movement_type="sale_cancellation",
                quantity=quantity_to_restore,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                description=(
                    f"Stock restored for cancelled "
                    f"Sale #{sale.id}. Reason: {reason}"
                )
            )

            db.add(movement)

        # Update the original sale record.
        sale.status = "cancelled"
        sale.cancelled_at = datetime.now(timezone.utc)
        sale.cancellation_reason = reason

        # Save everything in one transaction.
        db.commit()

        db.refresh(sale)

        return sale

    except Exception:
        db.rollback()
        raise
