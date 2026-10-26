from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.auth.password import hash_password
from app.core.database import get_db
from app.models.user import User
from app.auth.dependencies import require_roles
from app.schemas.user import AdminUserCreate, UserResponse



router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return{
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }

@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    return {
        "message": "Welcome, Admin!",
        "username": current_user.username,
        "role": current_user.role,
    }


@router.get("/management-test")
def management_test(
    current_user: User = Depends(
        require_roles("admin", "manager")
    ),
):
    return {
        "message": "Management access granted",
        "username": current_user.username,
        "role": current_user.role,
    }


@router.get("/staff-test")
def staff_test(
    current_user: User = Depends(
        require_roles("admin", "manager", "staff")
    ),
):
    return {
        "message": "Access granted",
        "username": current_user.username,
        "role": current_user.role,
    }



@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    # Only managers and staff may be created here.
    role = user_data.role.strip().lower()

    if role not in {"manager", "staff"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be manager or staff",
        )

    # Check for an existing email.
    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    # Check for an existing username.
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken",
        )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

