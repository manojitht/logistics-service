from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    stock_quantity: int = Field(ge=0, description="Stock cannot be negative")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
