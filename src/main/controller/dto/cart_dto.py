from pydantic import BaseModel, Field
from typing import Optional

class CartItemDTO(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the cart item")  # For updates
    user_id: Optional[int] = Field(None, description="Unique identifier for the user")
    product_id: int
    quantity: int

class NewCartItemDTO(BaseModel):
    product_id: int
    quantity: int