from sqlalchemy import Column, Integer, String, Numeric, Date
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    items = Column(String(1000), nullable=False)  # Store as comma-separated or JSON string
    total_price = Column(Numeric(10, 2))
    order_date = Column(Date)
