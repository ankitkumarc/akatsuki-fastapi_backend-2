from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from fastapi import UploadFile

class Type(str, Enum):
    product = 'product'
    entrance = 'entrance'

class SetupCameraSchema(BaseModel):
    zone_name: str = Field(...,description="zone-name")
    zone_image: str = Field(..., description = "zone-image")
    camera_id: str = Field(..., description = "camera-id")
    camera_type: Type

class SetupSchema(BaseModel):
    setup_id: UUID = Field(default_factory=uuid4, unique=True)
    shop_name: str 
    shop_manager_name: str
    coorporate_email: str
    phone_number: str
    address: str
    brand_logo: str
    description: str
    camera_zones: List[SetupCameraSchema]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True