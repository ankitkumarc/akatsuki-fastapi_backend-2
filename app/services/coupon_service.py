from typing import List
from uuid import UUID

from fastapi import HTTPException
from app.models.retailer_model import User
from app.models.coupon_model import Coupon
from beanie import Document
from app.schemas.coupon_schema import CouponCreate, CouponUpdate

class CouponService:
    @staticmethod
    async def list_coupons() -> List[Coupon]:
        return await Coupon.find_all().to_list()

    @staticmethod
    async def create_coupon(data: CouponCreate) -> Coupon:
        coupon = Coupon(**data.dict())
        return await coupon.insert()

    @staticmethod
    async def retrieve_coupon(coupon_id: UUID):
        return await Coupon.find_one(Coupon.coupon_id == coupon_id)

    @staticmethod
    async def update_coupon(coupon_id: UUID, data: CouponUpdate):
        coupon = await CouponService.retrieve_coupon(coupon_id)
        if coupon:
            await coupon.update({"$set": data.dict(exclude_unset=True)})
            await coupon.save()
        return coupon

    @staticmethod
    async def delete_coupon(coupon_id: UUID):
        deleted_coupon = await Coupon.find_one(Coupon.coupon_id == coupon_id)
        if deleted_coupon:
            await deleted_coupon.delete()
            return deleted_coupon
        else:
            raise HTTPException(status_code=404, detail="Coupon not found")