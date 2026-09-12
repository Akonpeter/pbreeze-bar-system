
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150,
    
    )

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=6,
        max_length=72,
    )

    role: str = "staff"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# from pydantic import BaseModel, EmailStr, Field



# class UserCreate(BaseModel):
#     full_name: str = Field(
#         min_length=2,
#         max_length=150.
#     )


#     email: EmailStr

#     username: str = Field(
#         min_length=3,
#         max_length=100,
#     )


#     password: str = Field(
#         min_length=6,
#         max_length=128,
#     )


#     role: str = "staff"


#     class Userlogin(BaseModel):
#         username: str
#         password: str



#     class UserResponse(BaseModel):
#         id: int
#         full_name: str
#         email: EmailStr
#         username: str
#         role: str
#         is_active: str


#     class config:
#         from_attributes = True



#     class TokenResponse(BaseModel):
#         access_token: str
#         token_type: str = "bearer"              