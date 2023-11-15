from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class DiscountType(str, Enum):
    percentage = 'percentage'
    fixed_amount = 'fixed_amount'

class CouponCreate(BaseModel):
    coupon_code: str = Field(..., description="Coupon Code", unique=True)
    description: str = Field(..., description="Coupon Description")
    discount_type: DiscountType
    coupon_amount: float 
    expiry_date: datetime
    prev_purchase_amount: float 
    visit_frequency: int


class CouponUpdate(BaseModel):
    coupon_code: Optional[str] = Field(..., description="Coupon Code")
    description: Optional[str] = Field(..., description="Coupon Description")
    discount_type: Optional[DiscountType]
    coupon_amount: Optional[float]
    expiry_date: Optional[datetime]
    prev_purchase_amount: Optional[float]
    visit_frequency: Optional[int]

class CouponOut(BaseModel):
    coupon_id: UUID
    coupon_code: str 
    description: str 
    discount_type: DiscountType
    coupon_amount: float 
    expiry_date: datetime
    prev_purchase_amount: float 
    visit_frequency: int
    created_at: datetime
    updated_at: datetime
