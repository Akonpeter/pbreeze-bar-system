
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Category, Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.auth.dependencies import get_current_user, require_roles

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),

):
    # Check whether the category exists.
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    # Check whether the SKU is already in use.
    if product_data.sku:
        existing_product = db.query(Product).filter(
            Product.sku == product_data.sku
        ).first()

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU already exists",
            )

    # Create the product.
    new_product = Product(**product_data.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# Create the GET /products/ endpoint.
@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    products = db.query(Product).order_by(Product.id).all()
    return products



@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product






@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    # Find the existing product.
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Get only the fields supplied by the user.
    update_data = product_data.model_dump(exclude_unset=True)

    # Check whether the new category exists.
    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"]
        ).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    # Check for duplicate SKU.
    if update_data.get("sku"):
        existing_product = db.query(Product).filter(
            Product.sku == update_data["sku"],
            Product.id != product_id,
        ).first()

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This SKU is already assigned to another product",
            )

    # Apply the updates.
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


