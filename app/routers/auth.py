from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.password import hash_password, verify_password
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Check email
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

    # Check username
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

    # Create user
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role.lower(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == login_data.username)
        .first()
    )

    if not user or not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.auth.jwt import create_access_token
# from app.auth.password import hash_password, verify_password
# from app.core.database import get_db
# from app.models.user import User
# from app.schemas.user import (
#     TokenResponse,
#     UserCreate,
#     UserLogin,
#     UserResponse,
# )


# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"],
# )


# @router.post(
#     "/register",
#     response_model=UserResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def register_user(
#     user_data: UserCreate,
#     db: Session = Depends(get_db),
# ):
#     # Check email
#     existing_email = (
#         db.query(User)
#         .filter(User.email == user_data.email)
#         .first()
#     )

#     if existing_email:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email is already registered",
#         )

#     # Check username
#     existing_username = (
#         db.query(User)
#         .filter(User.username == user_data.username)
#         .first()
#     )

#     if existing_username:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username is already taken",
#         )

#     # Create user
#     new_user = User(
#         full_name=user_data.full_name,
#         email=user_data.email,
#         username=user_data.username,
#         hashed_password=hash_password(user_data.password),
#         role=user_data.role.lower(),
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @router.post(
#     "/login",
#     response_model=TokenResponse,
# )
# def login_user(
#     login_data: UserLogin,
#     db: Session = Depends(get_db),
# ):
#     user = (
#         db.query(User)
#         .filter(User.username == login_data.username)
#         .first()
#     )

#     if not user or not verify_password(
#         login_data.password,
#         user.hashed_password,
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User account is inactive",
#         )

#     access_token = create_access_token(
#         data={
#             "sub": str(user.id),
#             "username": user.username,
#             "role": user.role,
#         }
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#     }