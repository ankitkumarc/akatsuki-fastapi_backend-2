from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class PurchaseCreate(BaseModel):
    product_name: str = Field(..., description="Product name")
    product_price: str = Field(..., description="Product price")
    customer_id: UUID = Field(..., description="Customer id")

class PurchaseOut(BaseModel):
    purchase_id: UUID
    product_name: str
    product_price: str
    customer_id: UUID
    created_at: datetime