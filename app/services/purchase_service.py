import datetime
from uuid import UUID
from typing import Dict, List
from datetime import datetime
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
    async def list_purchases_by_year(customer_id: UUID, year: int) -> Dict[int, float]:
        purchases = await Purchase.find(Purchase.customer_id == customer_id).to_list()

        if purchases:
            total_purchase_by_month = [0.0] * 12

            for purchase in purchases:
                if purchase.customer_id == customer_id and purchase.created_at.year == year:
                    product_price = float(purchase.product_price)
                    month = purchase.created_at.month
                    total_purchase_by_month[month-1] += product_price

            return total_purchase_by_month

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchases not found for the given customer {customer_id} and year {year}")
    @staticmethod
    async def list_purchases_by_month(customer_id: UUID, month: int) -> List[Purchase]:
        purchases = await Purchase.find(Purchase.customer_id == customer_id).to_list()
        filtered_purchases = [
            purchase for purchase in purchases
            if purchase.customer_id == customer_id and purchase.created_at.month == month
        ]
        return filtered_purchases
    @staticmethod
    async def create_purchase( data: PurchaseCreate) -> Purchase:
        purchase = Purchase(**data.dict())
        return await purchase.insert()
    
    
    
    