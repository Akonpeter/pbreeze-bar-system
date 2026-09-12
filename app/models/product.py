from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from app.core.database import Base





class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True)


    name = Column(
        String(150),
        nullable=False,
        index=True,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    sku = Column(
        String(100),
        unique=True,
        nullable=True,
    )

    cost_price = Column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    selling_price = Column(
        Numeric(12, 2),
        nullable=False,
    
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False,
       
    )

    def __repr__(self):
        return f"<Product {self.name}>"