from pydantic import Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from .retailer_model import User
from enum import Enum

class Gender(str, Enum):
    male = 'male'
    female = 'female'

class Customer(Document):
    class Settings:
        collection = 'customers'
    customer_id: UUID = Field(default_factory=uuid4, unique=True)
    phone_number: str = Indexed(unique=True)
    first_name: str
    last_name: str
    email: str = Indexed(unique=True)
    total_bill_amount: float
    visit_frequency: int
    address: str
    feedback: str
    gender : Gender
    age: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # owner: Link[User]

    def __hash__(self) -> int:
        return hash(self.customer_id)

    def __eq__(self, other: object)->bool:
        if isinstance(other, Customer):
            return self.customer_id == other.customer_id
        return False
    
    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()



