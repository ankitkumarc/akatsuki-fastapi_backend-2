from beanie import Document, Indexed
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime

class User(Document):
    class Settings:
        collection = 'retailsense' 

    user_id: UUID = Field(default_factory=uuid4)
    brand_name: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = Indexed(unique=True)
    phone_number: str = ""
    address: str = ""
    hashed_password: str = ""

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.user_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.user_id == other.user_id
        return False
  
    @property
    def created_at(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(cls, email: str) -> "User":
        return await cls.find_one(cls.email == email)
