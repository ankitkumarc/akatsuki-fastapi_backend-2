from uuid import UUID
from typing import List

from beanie import init_beanie
from fastapi import HTTPException, status
from app.models.purchase_model import Purchase
from app.models.customer_model import Customer
from app.schemas.purchase_schema import PurchaseCreate, PurchaseOut

class PurchaseService:
    @staticmethod
    async def list_purchases(customer_id:UUID)->List[Purchase]:
        purchases = await Purchase.find(Purchase.customer_id == customer_id).to_list()
        if purchases:
            return purchases
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchase not found")
    
    @staticmethod
    async def create_purchase( data: PurchaseCreate) -> Purchase:
        purchase = Purchase(**data.dict())
        return await purchase.insert()
    
    
    
    