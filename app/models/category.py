from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    description = Column(
        String(255),
        nullable=True,
    )

    products = relationship(
        "Product",
        back_populates="category",
    )

    def __repr__(self):
        return f"<Category {self.name}>"




# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from app.core.database import Base

# Base = declarative_base()

# class Category(Base):
#     __tablename__ = "categories"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     name = Column(
#         String(100),
#         unique=True,
#         nullable=False,
#     )

#     description = Column(
#         String(255),
#         nullable=True,
#     )

#     products = relationship(
#         "Product",
#         back_populates="category",
#     )

#     def __repr__(self):
#         return f"<Category {self.name}>"











