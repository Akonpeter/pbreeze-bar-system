from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base





class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    movement_type = Column(
        String(20),
        nullable=False
    )

    quantity = Column(
    Numeric(12, 2),
    nullable=False
    )

    previous_quantity = Column(
        Numeric(12, 2),
        nullable=False
    )

    new_quantity = Column(
        Numeric(12, 2),
        nullable=False
    )

    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    product = relationship(
        "Product", 
        back_populates="stock_movements"
        )

    def __repr__(self):
        return f"<StockMovement Product ID: {self.product_id}>"