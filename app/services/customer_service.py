import statistics
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from app.models.retailer_model import User
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate,CustomerOut

class CustomerService:
    @staticmethod
    async def list_customers()->List[CustomerOut]:
        customers = await Customer.find_all().to_list()
        return customers
    
    @staticmethod
    async def create_customer( data: CustomerCreate) -> Customer:
        existing_customer = await Customer.find_one(Customer.phone_number==data.phone_number)
        if existing_customer:
             raise ValueError("Customer with this phone already exists")
        
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
    async def update_customer(customer_id:UUID, data: CustomerUpdate):
        customer = await CustomerService.retrieve_customer( customer_id)
        if customer:
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
