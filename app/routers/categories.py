from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Category
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],



)

@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.id).all()


    return categories




class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)


@router.post("/")
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing_category = db.query(Category).filter(
        Category.name == category_data.name
    ).first()

    if existing_category:
        from fastapi import HTTPException


        raise HTTPException(
            status_code=409,
            detail="This category already exist",
        )
    new_category = Category(**category_data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

