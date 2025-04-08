from pydantic import BaseModel, Field
from typing import Optional

class ProductDTO(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the product")  # For updates
    name: str
    price: float
    image_url: str
    description: str

class NewProductDTO(BaseModel):
    name: str
    price: float
    image_url: str
    description: str