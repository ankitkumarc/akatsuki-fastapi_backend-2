from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.retailer_model import User
from app.models.customer_model import Customer
from app.models.coupon_model import Coupon
from app.core.config import settings
from app.api.api_v1.router import router 
from app.models.purchase_model import Purchase
from app.models.setup_model import Setup


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000","http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    """
    Initialize crucial application services
    """
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True).retailsense
    await init_beanie(
        database=db_client,
        document_models=[
            Customer,
            Coupon,
            Purchase,
            User,
            Setup,
        ]
    )


app.include_router(router, prefix=settings.API_V1_STR)