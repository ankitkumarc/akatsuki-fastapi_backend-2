from pydantic import Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from beanie import Document, Indexed

class DiscountType(str, Enum):
    percentage = 'percentage'
    fixed_amount = 'fixed_amount'

class Coupon(Document):
    class Settings:
        collection = 'coupons'
    
    coupon_id: UUID = Field(default_factory=uuid4)
    coupon_code: str = Indexed(unique=True)
    description: str
    discount_type: DiscountType
    coupon_amount: float 
    expiry_date: datetime
    prev_purchase_amount: float
    visit_frequency: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


    def __hash__(self) -> int:
        return hash(self.coupon_id)

    def __eq__(self, other: object)->bool:
        if isinstance(other, Coupon):
            return self.coupon_id == other.coupon_id
        return False