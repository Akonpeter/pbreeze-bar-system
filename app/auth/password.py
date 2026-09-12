from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plain-text password securely."""
    print("PASSWORD LENGTH:", len(password))
    print("PASSWORD BYTES:", len(password.encode("utf-8")))
    print("PASSWORD TYPE:", type(password))


    if len(password.encode("utf-8")) > 72:
        raise ValueError(
            "Password must not be longer than 72 bytes."
        )

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Check whether a plain password matches its hash."""

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# from passlib.context import CryptContext


# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto",
# )


# def hash_password(password: str) -> str:
#     if len(password.encode("utf-8")) > 72:
#         raise ValueError(
#             "Password must not be longer than 72 bytes."
#         )

#     return pwd_context.hash(password)


# def verify_password(
#     plain_password: str,
#     hashed_password: str,
# ) -> bool:
#     return pwd_context.verify(
#         plain_password,
#         hashed_password,
#     )



# # from passlib.context import CryptContext



# # pwd_context = CryptContext(
# # schemes=["bcrypt"],
# # deprecated="auto",


# # )



# # def hash_password(password: str) -> str:
# #     """Covert a plain password into a secure hash."""
# #     return pwd_context.hash(password)



# # def verify_password(
# #         plain_password: str,
# #         hashed_password: str,

# # ) -> bool:
# #     """Cheek whether a password matches its stored hash."""
# #     return pwd_context.verify(
# #         plain_password,
# #         hashed_password,
# #     )
