from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from beanie import Document
import json

class Type(str, Enum):
    product = 'product'
    entrance = 'entrance'

class SetupCamera(Document):
    zone_name: str
    zone_image: str
    camera_id: str
    camera_type: Type

class Setup(Document):
    setup_id: UUID = Field(default_factory=uuid4, unique=True)
    shop_name: str 
    shop_manager_name: str
    coorporate_email: str = Field(..., index=True, unique=True)
    phone_number: str = Field(..., index=True, unique=True)
    address: str
    brand_logo: str
    camera_zones: List[SetupCamera] = []  # Initialize as an empty list
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __hash__(self) -> int:
        return hash(self.setup_id)

    def __to_file(self, filename: str):
        with open(filename, "a") as file:
            file.write(json.dumps(self.dict(), default=str) + "\n")
