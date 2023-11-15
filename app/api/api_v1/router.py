from fastapi import APIRouter 
from app.api.api_v1.handlers import user
from app.api.auth.jwt import auth_router
from app.api.api_v1.handlers import customer
from app.api.api_v1.handlers import coupon
from app.api.api_v1.handlers import purchase
router = APIRouter()


router.include_router(user.user_router, tags=["user"]) 
router.include_router(auth_router, tags=["auth"])
router.include_router(customer.customer_router, prefix='/customer',tags=["customer"]) 
router.include_router(coupon.coupon_router, prefix='/coupon',tags=["coupon"]) 
router.include_router(purchase.purchase_router, prefix='/purchase',tags=["purchase"])
