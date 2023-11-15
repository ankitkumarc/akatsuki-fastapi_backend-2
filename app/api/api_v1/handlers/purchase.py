from fastapi import APIRouter, Depends
from app.schemas.purchase_schema import PurchaseOut, PurchaseCreate
from app.api.deps.retailer_deps import get_current_user,get_current_customer
from app.models.retailer_model import User  
from app.services.purchase_service import PurchaseService
from app.models.customer_model import Customer
from app.models.purchase_model import Purchase
from uuid import UUID
from typing import List

purchase_router = APIRouter()
@purchase_router.get('/{customer_id}', summary="Get All Purchases", response_model=List[Purchase])
async def list_purchases(customer_id: UUID):
    purchases = await PurchaseService.list_purchases(customer_id)
    return purchases

@purchase_router.post('/', summary="Create Purchase", response_model=Purchase)
async def create_purchase(data: PurchaseCreate):
    return await PurchaseService.create_purchase(data)