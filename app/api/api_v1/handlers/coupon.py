from fastapi import APIRouter, Depends
from app.schemas.coupon_schema import CouponOut, CouponCreate, CouponUpdate
from app.api.deps.retailer_deps import get_current_user
from app.models.retailer_model import User
from app.services.coupon_service import CouponService
from app.models.coupon_model import Coupon
from uuid import UUID
from typing import List

coupon_router = APIRouter()

@coupon_router.get("/", response_model=List[CouponOut])
async def list_coupons():
    return await CouponService.list_coupons()

@coupon_router.post("/", response_model=CouponOut)
async def create_coupon(data: CouponCreate):
    return await CouponService.create_coupon(data)

@coupon_router.get("/{coupon_id}", response_model=CouponOut)
async def retrieve_coupon(coupon_id: UUID):
    return await CouponService.retrieve_coupon(coupon_id)

@coupon_router.put("/{coupon_id}", response_model=CouponOut)
async def update_coupon(coupon_id: UUID, data: CouponUpdate):
    return await CouponService.update_coupon(coupon_id, data)

@coupon_router.delete("/{coupon_id}", response_model=CouponOut)
async def delete_coupon(coupon_id: UUID):
    return await CouponService.delete_coupon(coupon_id)