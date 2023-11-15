from fastapi import APIRouter
from app.schemas.user_schema import UserAuth, UserOut
from app.services.user_service import UserService
from fastapi import APIRouter, HTTPException, status
import pymongo


user_router = APIRouter()

@user_router.post("/signup", summary="signup a new user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserAuth):
    try:
       created_user = await UserService.create_user(data)
       return created_user
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )

    