from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserAuth(BaseModel):
    brand_name: str = Field(..., description="Brand name")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    email: EmailStr = Field(..., description="User email")
    phone_number: str = Field(..., description="User phone number")
    address: str = Field(..., description="User address")
    password: str = Field(...,min_length=5, description="user password")


class UserOut(BaseModel):
    user_id: UUID
    brand_name: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str


