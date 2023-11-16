from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class CustomerCreate(BaseModel):
    phone_number: str = Field(..., description="Customer phone number")
    first_name: str = Field(..., description="Customer first name")
    last_name: str = Field(..., description="Customer last name")
    email: EmailStr = Field(..., description="Customer email")
    bill_amount: float = Field(..., description="Customer bill amount")
    address: str = Field(..., description="Customer address")
    feedback: str = Field(None, description="Customer feedback")
    age: int = Field(...,description="Age of Customer")
    gender: Gender = Field(...,description="Gender of Customer")

class CustomerUpdate(BaseModel):
    phone_number: Optional[str] = Field(..., description="Customer phone number")
    first_name: Optional[str] = Field(..., description="Customer first name")
    last_name: Optional[str] = Field(..., description="Customer last name")
    email: Optional[EmailStr] = Field(..., description="Customer email")
    bill_amount: Optional[float] = Field(None, description="Customer bill amount")
    address: Optional[str] = Field(..., description="Customer address")
    feedback: Optional[str] = Field(None, description="Customer feedback")
    age: int = Field(..., description="Age of Customer")
    gender: Gender = Field(..., description="Gender of Customer")


class CustomerOut(BaseModel):
    customer_id: UUID
    phone_number: str  
    first_name: str 
    last_name: str 
    email: EmailStr 
    bill_amount: float
    address: str 
    feedback:str
    created_at: datetime
    updated_at: datetime
    age: int
    gender: Gender

