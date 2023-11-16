from typing import List
from uuid import UUID
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
        customer = Customer(**data.dict())
        return await customer.insert()
    
    @staticmethod
    async def retrieve_customer(customer_id:UUID):
        customer = await Customer.find_one(Customer.customer_id == customer_id)
        return customer
    
    @staticmethod
    async def retrieve_customer2(phone_number:str):
        customer = await Customer.find_one(Customer.phone_number == phone_number)
        if(customer):
            return customer
        else:
            return {}
    
    @staticmethod
    async def update_customer(customer_id:UUID, data: CustomerUpdate):
        customer = await CustomerService.retrieve_customer( customer_id)
        await customer.update({"$set": data.dict(exclude_unset=True)})
        await customer.save()
        return customer
    
    @staticmethod
    async def delete_customer(customer_id:UUID):
        customer = await CustomerService.retrieve_customer( customer_id)
        if customer:
            await customer.delete()

        return None
