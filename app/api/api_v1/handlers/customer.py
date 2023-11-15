from fastapi import APIRouter, Depends
from app.schemas.customer_schema import CustomerOut, CustomerCreate, CustomerUpdate
from app.api.deps.retailer_deps import get_current_user
from app.models.retailer_model import User
from app.services.customer_service import CustomerService
from app.models.customer_model import Customer
from uuid import UUID
from typing import List

customer_router = APIRouter()

@customer_router.get('/', summary="Get All Customers", response_model=List[CustomerOut])
async def list():
    return await CustomerService.list_customers()

@customer_router.post('/', summary="Create Customer", response_model=Customer)
async def create_customer(data: CustomerCreate):
    return await CustomerService.create_customer(data)

@customer_router.get('/{customer_id}', summary="Get a customer by customer_id", response_model=CustomerOut)
async def retrieve(customer_id: UUID):
    return await CustomerService.retrieve_customer( customer_id)

@customer_router.get('/retrieve/{phone_number}', summary="Get a customer by phone_number", response_model=CustomerOut)
async def retrieve(phone_number: str):
    return await CustomerService.retrieve_customer2( phone_number)


@customer_router.put('/{customer_id}', summary="Update customer by customer_id", response_model=CustomerOut)
async def update(customer_id: UUID, data: CustomerUpdate):
    return await CustomerService.update_customer( customer_id, data)


@customer_router.delete('/{customer_id}', summary="Delete customer by customer_id")
async def delete(customer_id: UUID):
    await CustomerService.delete_customer( customer_id)
    return None