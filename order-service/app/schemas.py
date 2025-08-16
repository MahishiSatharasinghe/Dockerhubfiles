from pydantic import BaseModel
from datetime import date
from typing import List

class OrderBase(BaseModel):
    customer_name: str
    items: List[str]
    total_price: float
    order_date: date

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
