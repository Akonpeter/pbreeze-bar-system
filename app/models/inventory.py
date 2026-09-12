from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(
        Integer,
        primary_key=True, 
        index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        unique=True,
        nullable=False,
    )

    quantity = Column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    minimum_stock = Column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    product = relationship(
        "Product",
        back_populates="inventory",
    )

    def __repr__(self):
        return f"<Inventory Product ID: {self.product_id}>"