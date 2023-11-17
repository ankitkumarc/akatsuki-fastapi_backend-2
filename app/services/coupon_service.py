from typing import List
from uuid import UUID

from fastapi import HTTPException,status
from app.models.customer_model import Customer
from app.models.retailer_model import User
from app.models.coupon_model import Coupon
from beanie import Document
from app.schemas.coupon_schema import CouponCreate, CouponUpdate

class CouponService:
    @staticmethod
    async def list_coupons(customer_id: UUID) -> List[Coupon]:
        customer = await Customer.find_one(Customer.customer_id == customer_id)
        if customer:
            coupons =  await Coupon.find((Coupon.visit_frequency <= customer.vist_frequency) & (customer.total_bill_amount>=Coupon.min_purchase_val)).to_list()
            if coupons:
                return coupons
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    @staticmethod
    async def create_coupon(data: CouponCreate) -> Coupon:
        try:
            coupon = Coupon(**data.dict())
            return await coupon.insert()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create coupon: {str(e)}")


    @staticmethod
    async def retrieve_coupon(coupon_id: UUID):
        coupon = await Coupon.find_one(Coupon.coupon_id == coupon_id)
        if coupon:
            return coupon
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")

    @staticmethod
    async def update_coupon(coupon_id: UUID, data: CouponUpdate):
        coupon = await CouponService.retrieve_coupon(coupon_id)
        if coupon:
            await coupon.update({"$set": data.dict(exclude_unset=True)})
            await coupon.save()
            return coupon
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
       

    @staticmethod
    async def delete_coupon(coupon_id: UUID):
        deleted_coupon = await Coupon.find_one(Coupon.coupon_id == coupon_id)
        if deleted_coupon:
            await deleted_coupon.delete()
            return deleted_coupon
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found or already deleted")