from pydantic import Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from .customer_model import Customer
      
class Purchase(Document):
    class Settings:
        collection = 'purchases'
    purchase_id: UUID = Field(default_factory=uuid4, unique=True)
    product_name: str
    product_price: str
    customer_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __hash__(self) -> int:
        return hash(self.purchase_id)

    def __eq__(self, other: object)->bool:
        if isinstance(other, Purchase):
            return self.purchase_id == other.purchase_id
        return False
