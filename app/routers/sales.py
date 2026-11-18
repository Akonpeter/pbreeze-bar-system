from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles

from app.schemas.sale import (
    SaleCreate,
    SaleResponse
)

from app.services.sale_service import create_sale





router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)



@router.post("/", response_model=SaleResponse)
def create_new_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return create_sale(db, sale_data)