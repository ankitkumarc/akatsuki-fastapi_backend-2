import statistics
from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from app.models.retailer_model import User
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate,CustomerOut
from app.services.purchase_service import PurchaseService

class CustomerService:
    @staticmethod
    async def list_customers()->List[CustomerOut]:
        customers = await Customer.find_all().to_list()
        return customers
    
    @staticmethod
    async def create_customer( data: CustomerCreate) -> Customer:
        existing_customer = await Customer.find_one(Customer.phone_number==data.phone_number)
        if existing_customer:
            raise HTTPException(status_code=statistics.HTTP_, detail="Customer with this phone already exists")
        
        data_dict = data.dict()
        data_dict.setdefault("visit_frequency", 1)
        customer = Customer(**data.dict())
        return await customer.insert()
    
    @staticmethod

    async def retrieve_customer(customer_id: UUID):
        customer = await Customer.find_one(Customer.customer_id == customer_id)
        if customer:
            return customer

        raise HTTPException(status_code=statistics.HTTP_404_NOT_FOUND, detail="Customer not found")

    @staticmethod
    async def retrieve_customer2(phone_number: str):
        customer = await Customer.find_one(Customer.phone_number == phone_number)
        if customer:
            return customer

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    
    @staticmethod
    async def update_customer(customer_id: UUID, data: CustomerUpdate):
        customer = await CustomerService.retrieve_customer(customer_id)
        if customer:
            if(data.total_bill_amount > 0):
                data.visit_frequency = customer.visit_frequency + 1
                
            data.total_bill_amount += customer.total_bill_amount
            
            await customer.update({"$set": data.dict(exclude_unset=True)})
            await customer.save()
            return customer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    
    @staticmethod
    async def delete_customer(customer_id:UUID):
        customer = await CustomerService.retrieve_customer( customer_id)
        if customer:
            await customer.delete()
            return ValueError("Customer is deleted")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    # @staticmethod
    # async def customer_purchase_year(year: int, customer_id) -> List[Customer]:
    #     # Retrieve customers whose purchase_date is in the specified year
    #     start_date = datetime(year, 1, 1)
    #     end_date = datetime(year, 12, 31)
    #     purchases = await PurchaseService.list_purchases()
    #     customers = await Customer.find(Customer.purchase_date >= start_date, Customer.purchase_date <= end_date).to_list()
    #     return customers