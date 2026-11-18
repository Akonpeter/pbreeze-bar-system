
from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base



class Sale(Base):
    __tablename__ = "sales"


    id = Column(Integer, primary_key=True, index=True)

    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    payment_method = Column(String(50), nullable=True)

    status = Column(String(20), nullable=False, default="completed")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan"
    )