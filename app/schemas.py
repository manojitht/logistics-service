from pydantic import BaseModel, Field, ConfigDict
from typing import List
from app.models import OrderStatus

class ProductBase(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    stock_quantity: int = Field(ge=0, description="Stock cannot be negative")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    product_id: int
    quantity_ordered: int
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    items: List[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)
    
class OrderUpdateStatus(BaseModel):
    status: OrderStatus

