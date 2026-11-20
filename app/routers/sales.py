from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.sale import SaleCancelRequest

from app.schemas.sale import (
    SaleCreate,
    SaleResponse
)

#from app.services.sale_service import create_sale
# from app.services.sale_service import (
#     create_sale,
#     get_all_sales
# )

from app.services.sale_service import (
    create_sale,
    get_all_sales,
    get_sale_by_id,
    cancel_sale
)





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


@router.post("/", response_model=SaleResponse)
def create_new_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return create_sale(db, sale_data)




@router.get("/", response_model=list[SaleResponse])
def read_sales(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return get_all_sales(db)




@router.get("/{sale_id}", response_model=SaleResponse)
def read_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return get_sale_by_id(db, sale_id)



@router.post("/{sale_id}/cancel", response_model=SaleResponse)
def cancel_existing_sale(
    sale_id: int,
    cancellation_data: SaleCancelRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    return cancel_sale(
        db,
        sale_id,
        cancellation_data
    )
