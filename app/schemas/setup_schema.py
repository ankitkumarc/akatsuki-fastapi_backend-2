from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class Type(str, Enum):
    product = 'product'
    entrance = 'entrance'

class SetupCameraSchema(BaseModel):
    zone_name: str = Field(...,description="zone-name")
    zone_image: str = Field(..., description = "zone-image")
    camera_id: str = Field(..., description = "camera-id")
    camera_type: Type

class SetupSchema(BaseModel):
    setup_id: UUID
    shop_name: str 
    shop_manager_name: str
    coorporate_email: str
    phone_number: str
    address: str
    brand_logo: str
    camera_zones: List[SetupCameraSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True