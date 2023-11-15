from app.schemas.user_schema import UserAuth, UserOut
from uuid import UUID
from app.models.retailer_model import User
from app.core.security import get_password, verify_password
from typing import Optional
import pymongo


class UserService:
    @staticmethod
    async def create_user(data: UserAuth) -> UserOut:
        user_in = User(
            brand_name=data.brand_name,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            address=data.address,
            phone_number=data.phone_number,
            hashed_password=get_password(data.password)
        )
        await user_in.save()
        return UserOut(
            user_id=user_in.user_id,
            brand_name=user_in.brand_name,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            phone_number=user_in.phone_number,
            address=user_in.address
        )
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user
    
   

        